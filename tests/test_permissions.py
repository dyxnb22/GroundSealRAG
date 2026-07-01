import pytest

from groundseal.evaluation.metrics import unauthorized_in_top_k
from groundseal.models.candidate import CandidateRecord
from groundseal.models.permission import PermissionDecision
from groundseal.models.source import utc_now_iso
from groundseal.permissions.filter import PermissionFilter
from groundseal.permissions.requester import RequesterContext
from groundseal.models.chunk import ChunkRecord
from groundseal.retrieval.pipeline import RetrievalResult


def _chunk(**kwargs) -> ChunkRecord:
    defaults = dict(
        chunk_id="CHK-test",
        document_id="DOC-1",
        source_id="SRC-1",
        text="secret data",
        start_offset=0,
        end_offset=10,
        heading_path=[],
        chunk_index=0,
        token_count=3,
        visibility="confidential",
        allowed_roles=["admin"],
        tenant_id="tenant-default",
    )
    defaults.update(kwargs)
    return ChunkRecord(**defaults)


def test_deny_missing_metadata():
    filt = PermissionFilter()
    chunk = _chunk(visibility="", allowed_roles=[])
    req = RequesterContext(requester_id="u1", roles=["admin"], allowed_visibilities=["confidential"])
    decision = filt.evaluate_chunk(chunk, req)
    assert decision.decision == "deny"
    assert decision.reason_code == "missing_metadata"


def test_tenant_mismatch_denied():
    filt = PermissionFilter()
    chunk = _chunk(tenant_id="tenant-a")
    req = RequesterContext(
        requester_id="u1",
        roles=["admin"],
        allowed_visibilities=["confidential"],
        tenant_id="tenant-b",
    )
    decision = filt.evaluate_chunk(chunk, req)
    assert decision.decision == "deny"
    assert decision.reason_code == "tenant_mismatch"


def test_contractor_explicit_source_grant():
    filt = PermissionFilter()
    chunk = _chunk(
        source_id="SRC-remote",
        visibility="general",
        allowed_roles=["engineer"],
    )
    req = RequesterContext(
        requester_id="contractor",
        roles=["contractor"],
        allowed_visibilities=["general"],
        allowed_source_ids=["SRC-remote"],
    )
    decision = filt.evaluate_chunk(chunk, req)
    assert decision.decision == "allow"


def test_unauthorized_in_top_k_no_double_count():
    cand = CandidateRecord(
        candidate_id="c1",
        query_id="q1",
        chunk_id="CHK-x",
        source_id="SRC-x",
        document_id="DOC-x",
        retrieval_method="lexical",
        raw_score=1.0,
        normalized_score=1.0,
        rank=1,
        retrieved_at=utc_now_iso(),
    )
    decision = PermissionDecision(
        chunk_id="CHK-x",
        requester_id="u1",
        decision="deny",
        reason_code="test",
        matched_rule="test",
        evaluated_at=utc_now_iso(),
    )
    result = RetrievalResult(
        query="q",
        requester_id="u1",
        method="hybrid",
        allowed_candidates=[cand],
        permission_decisions=[decision],
    )
    assert unauthorized_in_top_k(result, k=5) == 1
