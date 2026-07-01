from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from groundseal.bootstrap import bootstrap, clear_pipeline_cache
from groundseal.chunking.baseline import CHUNK_STRATEGIES
from groundseal.evaluation.runner import EvalRunner
from groundseal.paths import ProjectPaths
from groundseal.pipeline.build import rebuild_chunks


@dataclass
class ChunkStrategyResult:
    strategy: str
    chunk_size: int
    overlap: int
    chunk_count: int
    avg_recall: float
    avg_mrr: float
    passed: int
    failed: int
    total_unauthorized: int
    total_leakage: int


def run_chunk_size_experiment(
    paths: ProjectPaths,
    strategies: list[str] | None = None,
    cases_dir: Path | None = None,
) -> list[ChunkStrategyResult]:
    strategies = strategies or ["baseline-384", "baseline-512", "baseline-768"]
    cases_dir = cases_dir or paths.cases_dir
    results: list[ChunkStrategyResult] = []

    for strategy in strategies:
        if strategy not in CHUNK_STRATEGIES:
            raise ValueError(f"Unknown strategy: {strategy}")

        chunk_count = rebuild_chunks(paths, strategy=strategy)
        clear_pipeline_cache()
        pipeline = bootstrap(paths, force_rebuild=True)
        runner = EvalRunner(pipeline, paths.personas_dir)
        report = runner.run_suite(cases_dir)

        size, overlap = CHUNK_STRATEGIES[strategy]
        results.append(
            ChunkStrategyResult(
                strategy=strategy,
                chunk_size=size,
                overlap=overlap,
                chunk_count=chunk_count,
                avg_recall=report.avg_recall,
                avg_mrr=report.avg_mrr,
                passed=report.passed,
                failed=report.failed,
                total_unauthorized=report.total_unauthorized,
                total_leakage=report.total_leakage,
            )
        )

    return results


def write_chunk_experiment_report(results: list[ChunkStrategyResult], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Chunk Size Experiment Report",
        "",
        "## Purpose",
        "Compare retrieval metrics across chunk size strategies on the same eval suite.",
        "",
        "## Results",
        "",
        "| strategy | size | overlap | chunks | recall@k | MRR | passed | unauthorized |",
        "|----------|------|---------|--------|----------|-----|--------|--------------|",
    ]
    for r in results:
        lines.append(
            f"| {r.strategy} | {r.chunk_size} | {r.overlap} | {r.chunk_count} | "
            f"{r.avg_recall:.3f} | {r.avg_mrr:.3f} | {r.passed}/{r.passed + r.failed} | {r.total_unauthorized} |"
        )

    best = max(results, key=lambda r: (r.avg_mrr, r.avg_recall))
    lines.extend(
        [
            "",
            f"## Conclusion",
            "",
            f"Best MRR on this suite: **{best.strategy}** (size={best.chunk_size}, overlap={best.overlap}).",
            "",
            "Follow-up: adopt winner as default only if permission and citation metrics remain zero.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    path.with_suffix(".json").write_text(
        json.dumps([r.__dict__ for r in results], indent=2),
        encoding="utf-8",
    )
