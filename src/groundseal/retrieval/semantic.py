from __future__ import annotations

import uuid
from dataclasses import replace

import numpy as np

from groundseal.models.candidate import CandidateRecord
from groundseal.models.source import utc_now_iso
from groundseal.retrieval.embeddings import EmbeddingModel, VectorIndex


class SemanticRetriever:
    def __init__(self, index: VectorIndex, model: EmbeddingModel) -> None:
        self.index = index
        self.model = model

    def search(self, query: str, top_k: int = 10, query_id: str | None = None) -> list[CandidateRecord]:
        if not self.index.chunks:
            return []

        qid = query_id or str(uuid.uuid4())
        query_vec = self.model.encode([query])[0]
        scores = self.index.embeddings @ query_vec
        ranked = np.argsort(scores)[::-1][:top_k]

        max_score = float(scores[ranked[0]]) if len(ranked) else 1.0
        candidates: list[CandidateRecord] = []
        for rank, idx in enumerate(ranked, start=1):
            raw_score = float(scores[idx])
            chunk = self.index.chunks[int(idx)]
            candidates.append(
                CandidateRecord(
                    candidate_id=f"CAND-sem-{uuid.uuid4().hex[:8]}",
                    query_id=qid,
                    chunk_id=chunk.chunk_id,
                    source_id=chunk.source_id,
                    document_id=chunk.document_id,
                    retrieval_method="semantic",
                    raw_score=raw_score,
                    normalized_score=raw_score / max_score if max_score else 0.0,
                    rank=rank,
                    retrieved_at=utc_now_iso(),
                    query_text=query,
                )
            )
        return candidates
