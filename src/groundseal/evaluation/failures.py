from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from groundseal.evaluation.runner import CaseResult
from groundseal.evaluation.schema import EvalCase


FAILURE_CATEGORIES = {
    "lexical": "lexical_miss",
    "semantic": "semantic_miss",
    "permission": "permission_false_allow",
    "citation": "citation_failure",
    "hybrid": "hybrid_merge_failure",
    "ranking": "ranking_failure",
    "generation": "evaluation_gap",
    "audit": "metadata_gap",
    "freshness": "metadata_gap",
}


def write_failure_record(
    case_result: CaseResult,
    case_id: str,
    query: str,
    requester_id: str,
    category: str,
    failures_dir: Path,
    expected: str = "",
    observed: str = "",
) -> Path:
    failures_dir.mkdir(parents=True, exist_ok=True)
    failure_id = f"FAIL-{case_id}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    path = failures_dir / f"{failure_id}.md"
    cat = FAILURE_CATEGORIES.get(category, "evaluation_gap")
    content = f"""# Failure: {failure_id}

- Phase: evaluation
- Date: {datetime.now(timezone.utc).isoformat()}
- Severity: high if permission else medium
- Query: {query}
- Requester: {requester_id}
- Expected: {expected or 'case pass'}
- Observed: {observed or f'recall={case_result.recall_at_5}, unauthorized={case_result.unauthorized}'}
- Category: {cat}
- Likely cause: retrieval or permission mismatch
- Proposed follow-up: re-run case after fix
- Status: open
"""
    path.write_text(content, encoding="utf-8")
    return path


def process_failed_cases(
    case_results: list[CaseResult],
    cases_map: dict[str, EvalCase],
    failures_dir: Path,
) -> list[Path]:
    written: list[Path] = []
    for result in case_results:
        if not result.passed:
            case = cases_map.get(result.case_id)
            if case:
                path = write_failure_record(
                    result,
                    case.case_id,
                    case.query,
                    case.requester_id,
                    case.category,
                    failures_dir,
                )
                written.append(path)
    return written
