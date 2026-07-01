from __future__ import annotations

from groundseal.evaluation.schema import EvalCase
from groundseal.retrieval.pipeline import RetrievalResult


def recall_at_k(result: RetrievalResult, case: EvalCase, k: int = 5) -> float:
    if case.expected_inaccessible:
        return 1.0 if not result.allowed_candidates[:k] else 0.0

    if not case.expected_source_ids:
        return 0.0

    allowed_sources = {c.source_id for c in result.allowed_candidates[:k]}
    hits = sum(1 for sid in case.expected_source_ids if sid in allowed_sources)
    return hits / len(case.expected_source_ids)


def mrr(result: RetrievalResult, case: EvalCase) -> float:
    if case.expected_inaccessible:
        return 1.0 if not result.allowed_candidates else 0.0

    for rank, cand in enumerate(result.allowed_candidates, start=1):
        if cand.source_id in case.expected_source_ids:
            return 1.0 / rank
        if case.expected_chunk_ids and cand.chunk_id in case.expected_chunk_ids:
            return 1.0 / rank
    return 0.0


def unauthorized_in_top_k(result: RetrievalResult, k: int = 5) -> int:
    count = 0
    for cand in result.allowed_candidates[:k]:
        decision = next((d for d in result.permission_decisions if d.chunk_id == cand.chunk_id), None)
        if decision and decision.decision != "allow":
            count += 1
    # also check if denied sources appear in allowed list (false allow)
    for cand in result.allowed_candidates[:k]:
        denied = any(d.chunk_id == cand.chunk_id and d.decision == "deny" for d in result.permission_decisions)
        if denied:
            count += 1
    return count


def citation_coverage(result: RetrievalResult, case: EvalCase) -> float:
    if not result.citation_package or case.expected_inaccessible:
        return 1.0 if (not result.citation_package or not result.citation_package.citations) else 0.0

    if not case.expected_source_ids:
        return 0.0

    cited = {c.source_id for c in result.citation_package.citations}
    hits = sum(1 for sid in case.expected_source_ids if sid in cited)
    return hits / len(case.expected_source_ids)


def inaccessible_citation_leakage(result: RetrievalResult) -> int:
    if not result.citation_package:
        return 0
    return sum(1 for c in result.citation_package.citations if c.permission_decision != "allow")
