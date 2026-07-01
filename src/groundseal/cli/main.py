from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer

from groundseal.audit.logger import AuditLogger
from groundseal.bootstrap import bootstrap
from groundseal.evaluation.failures import process_failed_cases
from groundseal.evaluation.runner import EvalRunner
from groundseal.evaluation.schema import load_cases
from groundseal.generation.grounded import GroundedGenerator
from groundseal.paths import ProjectPaths, find_project_root
from groundseal.permissions.requester import load_requester
from groundseal.registry.store import SourceRegistry

app = typer.Typer(help="GroundSeal RAG — permission-aware hybrid retrieval")


def _paths() -> ProjectPaths:
    return ProjectPaths(find_project_root())


@app.command("register-source")
def register_source(
    manifest: Path = typer.Option(None, "--manifest", help="Path to manifest.yaml"),
) -> None:
    paths = _paths()
    registry = SourceRegistry(paths.registry_dir)
    m = manifest or paths.manifest
    sources = registry.register_from_manifest(m)
    typer.echo(json.dumps([s.to_dict() for s in sources], indent=2))


@app.command("ingest")
def ingest(
    source_id: Optional[str] = typer.Option(None, "--source-id"),
    all_sources: bool = typer.Option(False, "--all"),
) -> None:
    from groundseal.ingestion.markdown_ingestor import MarkdownIngestor

    paths = _paths()
    registry = SourceRegistry(paths.registry_dir)
    ingestor = MarkdownIngestor(registry, paths.corpus)

    if all_sources or not source_id:
        docs = ingestor.ingest_all(paths.sources_dir)
    else:
        path = next(paths.sources_dir.glob("*.md"), None)
        for p in paths.sources_dir.glob("*.md"):
            meta, _ = __import__("groundseal.ingestion.markdown_ingestor", fromlist=["parse_markdown"]).parse_markdown(p)
            if meta.get("source_id") == source_id:
                path = p
                break
        if path is None:
            raise typer.Exit(1)
        docs = [ingestor.ingest_file(path, source_id)]

    typer.echo(json.dumps([d.to_dict() for d in docs], indent=2))


@app.command("chunk")
def chunk(
    strategy: str = typer.Option("baseline", "--strategy"),
) -> None:
    from groundseal.ingestion.markdown_ingestor import MarkdownIngestor

    paths = _paths()
    registry = SourceRegistry(paths.registry_dir)
    ingestor = MarkdownIngestor(registry, paths.corpus)
    chunker = __import__("groundseal.chunking.baseline", fromlist=["BaselineChunker"]).BaselineChunker(registry)

    docs = registry.list_documents()
    chunks = chunker.chunk_all(docs, lambda doc: ingestor.get_body(doc))
    chunker.save_chunks(chunks, paths.chunks_path)
    typer.echo(json.dumps({"chunk_count": len(chunks), "strategy": strategy}))


@app.command("retrieve")
def retrieve(
    query: str = typer.Option(..., "-q", "--query"),
    requester: str = typer.Option(..., "-r", "--requester"),
    method: str = typer.Option("hybrid", "--method"),
    top_k: int = typer.Option(10, "--top-k"),
    pack: bool = typer.Option(False, "--pack"),
    rerank: bool = typer.Option(False, "--rerank"),
) -> None:
    paths = _paths()
    pipeline = bootstrap(paths)
    req = load_requester(paths.personas_dir, requester)
    result = pipeline.retrieve(query, req, method=method, top_k=top_k, pack=pack, rerank=rerank)

    audit = AuditLogger(paths.audit_log)
    audit.log_retrieval(
        {
            "query": query,
            "requester": requester,
            "method": method,
            "allowed_count": len(result.allowed_candidates),
            "denied_count": len(result.denied_candidates),
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
) -> None:
    paths = _paths()
    pipeline = bootstrap(paths)
    runner = EvalRunner(pipeline, paths.personas_dir)
    cases_dir = suite or paths.cases_dir
    eval_report = runner.run_suite(cases_dir, method=method)

    report_path = report or paths.reports_dir / "phase9-eval-suite-report.md"
    runner.write_report(eval_report, report_path)

    cases = load_cases(cases_dir)
    cases_map = {c.case_id: c for c in cases}
    process_failed_cases(eval_report.case_results, cases_map, paths.failures_dir)

    if eval_report.total_unauthorized > 0:
        typer.echo("BLOCKING: unauthorized_in_top_k > 0", err=True)
        raise typer.Exit(1)

    typer.echo(json.dumps({"passed": eval_report.passed, "failed": eval_report.failed, "report": str(report_path)}))


@app.command("report")
def report(
    failures: bool = typer.Option(False, "--failures"),
    phase: Optional[int] = typer.Option(None, "--phase"),
) -> None:
    paths = _paths()
    if failures:
        fail_dir = paths.failures_dir
        files = list(fail_dir.glob("*.md")) if fail_dir.exists() else []
        typer.echo(json.dumps({"failure_records": [str(f) for f in files], "count": len(files)}))
    elif phase:
        report_file = paths.reports_dir / f"phase{phase}-report.md"
        alt = list(paths.reports_dir.glob(f"phase{phase}-*.md"))
        target = alt[0] if alt else report_file
        if target.exists():
            typer.echo(target.read_text(encoding="utf-8"))
        else:
            typer.echo(f"No report for phase {phase}", err=True)
            raise typer.Exit(1)
    else:
        reports = [str(p) for p in paths.reports_dir.glob("phase*.md")]
        typer.echo(json.dumps({"reports": reports}))


@app.command("answer")
def answer(
    query: str = typer.Option(..., "-q", "--query"),
    requester: str = typer.Option(..., "-r", "--requester"),
    method: str = typer.Option("hybrid", "--method"),
) -> None:
    paths = _paths()
    pipeline = bootstrap(paths)
    req = load_requester(paths.personas_dir, requester)
    result = pipeline.retrieve(query, req, method=method, top_k=10, pack=True)
    gen = GroundedGenerator()
    if result.citation_package:
        output = gen.generate(result.citation_package)
        typer.echo(json.dumps(output, indent=2))
    else:
        typer.echo(json.dumps({"status": "no_package"}))


if __name__ == "__main__":
    app()
