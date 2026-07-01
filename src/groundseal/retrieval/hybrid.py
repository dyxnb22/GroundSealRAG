from __future__ import annotations

import uuid
from collections import defaultdict

from groundseal.models.candidate import CandidateRecord
from groundseal.models.source import utc_now_iso
from groundseal.retrieval.lexical import LexicalRetriever
from groundseal.retrieval.semantic import SemanticRetriever

RRF_K = 60


def reciprocal_rank_fusion(
    result_lists: list[list[CandidateRecord]],
    top_k: int = 10,
    query: str = "",
    query_id: str | None = None,
) -> list[CandidateRecord]:
    qid = query_id or str(uuid.uuid4())
    scores: dict[str, float] = defaultdict(float)
    chunk_map: dict[str, CandidateRecord] = {}
    methods: dict[str, set[str]] = defaultdict(set)

    for results in result_lists:
        for cand in results:
            scores[cand.chunk_id] += 1.0 / (RRF_K + cand.rank)
            methods[cand.chunk_id].add(cand.retrieval_method)
            if cand.chunk_id not in chunk_map:
                chunk_map[cand.chunk_id] = cand

    ranked_ids = sorted(scores.keys(), key=lambda cid: scores[cid], reverse=True)[:top_k]
    max_score = scores[ranked_ids[0]] if ranked_ids else 1.0

    merged: list[CandidateRecord] = []
    for rank, cid in enumerate(ranked_ids, start=1):
        base = chunk_map[cid]
        method_label = "+".join(sorted(methods[cid]))
        merged.append(
            CandidateRecord(
                candidate_id=f"CAND-hyb-{uuid.uuid4().hex[:8]}",
                query_id=qid,
                chunk_id=base.chunk_id,
                source_id=base.source_id,
                document_id=base.document_id,
                retrieval_method=f"hybrid({method_label})",
                raw_score=scores[cid],
                normalized_score=scores[cid] / max_score if max_score else 0.0,
                rank=rank,
                retrieved_at=utc_now_iso(),
                query_text=query,
            )
        )
    return merged


class HybridRetriever:
    def __init__(self, lexical: LexicalRetriever, semantic: SemanticRetriever) -> None:
        self.lexical = lexical
        self.semantic = semantic

    def search(self, query: str, top_k: int = 10, query_id: str | None = None) -> list[CandidateRecord]:
        qid = query_id or str(uuid.uuid4())
        lex = self.lexical.search(query, top_k=top_k * 2, query_id=qid)
        sem = self.semantic.search(query, top_k=top_k * 2, query_id=qid)
        return reciprocal_rank_fusion([lex, sem], top_k=top_k, query=query, query_id=qid)
