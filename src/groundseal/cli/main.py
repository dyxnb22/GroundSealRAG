from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer

from groundseal.audit.logger import AuditLogger
from groundseal.bootstrap import bootstrap, clear_pipeline_cache
from groundseal.chunking.baseline import BaselineChunker, STRATEGIES
from groundseal.evaluation.failures import process_failed_cases
from groundseal.evaluation.runner import EvalRunner
from groundseal.evaluation.schema import load_cases
from groundseal.generation.grounded import GroundedGenerator
from groundseal.ingestion.markdown_ingestor import MarkdownIngestor, parse_markdown
from groundseal.paths import ProjectPaths, find_project_root
from groundseal.permissions.requester import load_requester
from groundseal.registry.store import RegistryError, SourceRegistry

app = typer.Typer(help="GroundSeal RAG — permission-aware hybrid retrieval")


def _paths() -> ProjectPaths:
    return ProjectPaths(find_project_root())


def _load_requester_or_exit(paths: ProjectPaths, requester_id: str):
    try:
        return load_requester(paths.personas_dir, requester_id)
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc


@app.command("register-source")
def register_source(
    manifest: Path = typer.Option(None, "--manifest", help="Path to manifest.yaml"),
) -> None:
    paths = _paths()
    registry = SourceRegistry(paths.registry_dir)
    try:
        sources = registry.register_from_manifest(manifest or paths.manifest)
    except RegistryError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc
    typer.echo(json.dumps([s.to_dict() for s in sources], indent=2))


@app.command("ingest")
def ingest(
    source_id: Optional[str] = typer.Option(None, "--source-id"),
    all_sources: bool = typer.Option(False, "--all"),
) -> None:
    if not all_sources and not source_id:
        typer.echo("Specify --all or --source-id", err=True)
        raise typer.Exit(1)

    paths = _paths()
    registry = SourceRegistry(paths.registry_dir)
    ingestor = MarkdownIngestor(registry, paths.root)

    if all_sources:
        docs = ingestor.ingest_all(paths.sources_dir)
    else:
        match_path: Path | None = None
        for path in paths.sources_dir.glob("*.md"):
            meta, _ = parse_markdown(path)
            if meta.get("source_id") == source_id:
                match_path = path
                break
        if match_path is None:
            typer.echo(f"No markdown file for source_id: {source_id}", err=True)
            raise typer.Exit(1)
        docs = [ingestor.ingest_file(match_path, source_id)]

    clear_pipeline_cache()
    typer.echo(json.dumps([d.to_dict() for d in docs], indent=2))


@app.command("chunk")
def chunk(
    strategy: str = typer.Option("baseline", "--strategy"),
    force: bool = typer.Option(False, "--force", help="Rebuild chunks even if fingerprint matches"),
) -> None:
    if strategy not in STRATEGIES:
        typer.echo(f"Unknown strategy: {strategy}. Choose from {sorted(STRATEGIES)}", err=True)
        raise typer.Exit(1)

    paths = _paths()
    registry = SourceRegistry(paths.registry_dir)
    ingestor = MarkdownIngestor(registry, paths.root)
    chunker = BaselineChunker(registry)

    documents = registry.list_documents()
    if not documents:
        typer.echo("No documents ingested. Run: groundseal ingest --all", err=True)
        raise typer.Exit(1)

    chunks = chunker.chunk_all(documents, ingestor.get_body, strategy=strategy)
    chunker.save_chunks(chunks, paths.chunks_path)
    clear_pipeline_cache()
    typer.echo(json.dumps({"chunk_count": len(chunks), "strategy": strategy}))


@app.command("retrieve")
def retrieve(
    query: str = typer.Option(..., "-q", "--query"),
    requester: str = typer.Option(..., "-r", "--requester"),
    method: str = typer.Option("hybrid", "--method"),
    top_k: int = typer.Option(10, "--top-k"),
    pack: bool = typer.Option(False, "--pack"),
    rerank: bool = typer.Option(False, "--rerank"),
    exclude_stale: bool = typer.Option(False, "--exclude-stale"),
) -> None:
    paths = _paths()
    try:
        pipeline = bootstrap(paths)
        req = _load_requester_or_exit(paths, requester)
        result = pipeline.retrieve(
            query,
            req,
            method=method,
            top_k=top_k,
            pack=pack,
            rerank=rerank,
            exclude_stale=exclude_stale,
        )
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc

    AuditLogger(paths.audit_log).log_retrieval(
        {
            "query": query,
            "requester": requester,
            "method": method,
            "allowed_count": len(result.allowed_candidates),
            "denied_count": len(result.denied_candidates),
            "stale_excluded": result.stale_excluded,
        }
    )

    if pack and result.citation_package:
        typer.echo(json.dumps(result.citation_package.to_dict(), indent=2))
    else:
        typer.echo(json.dumps([c.to_dict() for c in result.allowed_candidates], indent=2))


@app.command("evaluate")
def evaluate(
    suite: Path = typer.Option(None, "--suite"),
    method: str = typer.Option("hybrid", "--method"),
    report: Path = typer.Option(None, "--report"),
    exclude_stale: bool = typer.Option(False, "--exclude-stale"),
) -> None:
    paths = _paths()
    pipeline = bootstrap(paths)
    runner = EvalRunner(pipeline, paths.personas_dir, exclude_stale=exclude_stale)
    cases_dir = suite or paths.cases_dir
    eval_report = runner.run_suite(cases_dir, method=method)

    report_path = report or paths.reports_dir / "phase9-eval-suite-report.md"
    runner.write_report(eval_report, report_path)

    cases_map = {c.case_id: c for c in load_cases(cases_dir)}
    process_failed_cases(eval_report.case_results, cases_map, paths.failures_dir)

    blocking = False
    if eval_report.total_unauthorized > 0:
        typer.echo("BLOCKING: unauthorized_in_top_k > 0", err=True)
        blocking = True
    if eval_report.total_leakage > 0:
        typer.echo("BLOCKING: citation_leakage > 0", err=True)
        blocking = True
    if eval_report.failed > 0:
        typer.echo(f"FAILURES: {eval_report.failed} case(s) did not pass", err=True)
        blocking = True

    if blocking:
        raise typer.Exit(1)

    typer.echo(
        json.dumps(
            {"passed": eval_report.passed, "failed": eval_report.failed, "report": str(report_path)}
        )
    )


@app.command("report")
def report_cmd(
    failures: bool = typer.Option(False, "--failures"),
    phase: Optional[int] = typer.Option(None, "--phase"),
) -> None:
    paths = _paths()
    if failures:
        fail_dir = paths.failures_dir
        files = sorted(fail_dir.glob("*.md")) if fail_dir.exists() else []
        typer.echo(json.dumps({"failure_records": [str(f) for f in files], "count": len(files)}))
    elif phase is not None:
        exact = paths.reports_dir / f"phase{phase}-report.md"
        if exact.exists():
            typer.echo(exact.read_text(encoding="utf-8"))
            return
        matches = sorted(paths.reports_dir.glob(f"phase{phase}-*.md"))
        if matches:
            typer.echo(matches[0].read_text(encoding="utf-8"))
            return
        typer.echo(f"No report for phase {phase}", err=True)
        raise typer.Exit(1)
    else:
        reports = sorted(str(p) for p in paths.reports_dir.glob("phase*.md"))
        typer.echo(json.dumps({"reports": reports}))


@app.command("answer")
def answer(
    query: str = typer.Option(..., "-q", "--query"),
    requester: str = typer.Option(..., "-r", "--requester"),
    method: str = typer.Option("hybrid", "--method"),
) -> None:
    paths = _paths()
    try:
        pipeline = bootstrap(paths)
        req = _load_requester_or_exit(paths, requester)
        result = pipeline.retrieve(query, req, method=method, top_k=10, pack=True)
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc

    if result.citation_package:
        output = GroundedGenerator().generate(result.citation_package)
        typer.echo(json.dumps(output, indent=2))
    else:
        typer.echo(json.dumps({"status": "no_package"}))


if __name__ == "__main__":
    app()
