from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from groundseal.evaluation.metrics import (
    citation_coverage,
    inaccessible_citation_leakage,
    mrr,
    recall_at_k,
    unauthorized_in_top_k,
)
from groundseal.evaluation.schema import EvalCase, load_cases
from groundseal.permissions.requester import load_requester
from groundseal.retrieval.pipeline import RetrievalPipeline


@dataclass
class CaseResult:
    case_id: str
    recall_at_5: float
    mrr: float
    unauthorized: int
    citation_coverage: float
    citation_leakage: int
    passed: bool
    notes: str = ""


@dataclass
class EvalReport:
    method: str
    total_cases: int
    passed: int
    failed: int
    avg_recall: float
    avg_mrr: float
    total_unauthorized: int
    total_leakage: int
    case_results: list[CaseResult] = field(default_factory=list)


class EvalRunner:
    def __init__(
        self,
        pipeline: RetrievalPipeline,
        personas_dir: Path,
        exclude_stale: bool = False,
    ) -> None:
        self.pipeline = pipeline
        self.personas_dir = personas_dir
        self.exclude_stale = exclude_stale

    def run_case(self, case: EvalCase, method: str | None = None) -> CaseResult:
        requester = load_requester(self.personas_dir, case.requester_id)
        effective_method = case.method if case.method != "hybrid" else (method or case.method)
        result = self.pipeline.retrieve(
            case.query,
            requester,
            method=effective_method,
            top_k=case.top_k,
            pack=True,
            exclude_stale=self.exclude_stale,
        )

        rec = recall_at_k(result, case, k=case.top_k)
        mrr_val = mrr(result, case)
        unauth = unauthorized_in_top_k(result, k=case.top_k)
        cite_cov = citation_coverage(result, case)
        leakage = inaccessible_citation_leakage(result)

        passed = unauth == 0 and leakage == 0
        if case.expected_inaccessible:
            passed = passed and rec >= 1.0
        elif case.expected_source_ids:
            passed = passed and rec > 0

        return CaseResult(
            case_id=case.case_id,
            recall_at_5=rec,
            mrr=mrr_val,
            unauthorized=unauth,
            citation_coverage=cite_cov,
            citation_leakage=leakage,
            passed=passed,
        )

    def run_suite(self, cases_dir: Path, method: str = "hybrid") -> EvalReport:
        cases = load_cases(cases_dir)
        results = [self.run_case(c, method=method) for c in cases]

        passed = sum(1 for r in results if r.passed)
        return EvalReport(
            method=method,
            total_cases=len(results),
            passed=passed,
            failed=len(results) - passed,
            avg_recall=sum(r.recall_at_5 for r in results) / len(results) if results else 0,
            avg_mrr=sum(r.mrr for r in results) / len(results) if results else 0,
            total_unauthorized=sum(r.unauthorized for r in results),
            total_leakage=sum(r.citation_leakage for r in results),
            case_results=results,
        )

    def write_report(self, report: EvalReport, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Evaluation Suite Report",
            "",
            f"- Method: {report.method}",
            f"- Total cases: {report.total_cases}",
            f"- Passed: {report.passed}",
            f"- Failed: {report.failed}",
            f"- Avg Recall@5: {report.avg_recall:.3f}",
            f"- Avg MRR: {report.avg_mrr:.3f}",
            f"- Unauthorized in top-k: {report.total_unauthorized}",
            f"- Citation leakage: {report.total_leakage}",
            "",
            "## Case Results",
            "",
            "| case_id | recall@5 | mrr | unauthorized | passed |",
            "|---------|----------|-----|--------------|--------|",
        ]
        for r in report.case_results:
            lines.append(
                f"| {r.case_id} | {r.recall_at_5:.2f} | {r.mrr:.2f} | {r.unauthorized} | {r.passed} |"
            )
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        json_path = path.with_suffix(".json")
        json_path.write_text(
            json.dumps(
                {
                    "method": report.method,
                    "total_cases": report.total_cases,
                    "passed": report.passed,
                    "failed": report.failed,
                    "avg_recall": report.avg_recall,
                    "avg_mrr": report.avg_mrr,
                    "total_unauthorized": report.total_unauthorized,
                    "total_leakage": report.total_leakage,
                    "cases": [r.__dict__ for r in report.case_results],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
