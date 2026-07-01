from __future__ import annotations

from dataclasses import replace

from groundseal.models.candidate import CandidateRecord
from groundseal.models.chunk import ChunkRecord

DEFAULT_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

_RERANKER_CACHE: dict[str, object] = {}


class CrossEncoderReranker:
    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        self.model_name = model_name

    @property
    def model(self):
        if self.model_name not in _RERANKER_CACHE:
            from sentence_transformers import CrossEncoder

            _RERANKER_CACHE[self.model_name] = CrossEncoder(self.model_name)
        return _RERANKER_CACHE[self.model_name]

    def rerank(
        self,
        query: str,
        candidates: list[CandidateRecord],
        chunk_map: dict[str, ChunkRecord],
    ) -> list[CandidateRecord]:
        if not candidates:
            return []

        pairs = []
        valid: list[CandidateRecord] = []
        for cand in candidates:
            chunk = chunk_map.get(cand.chunk_id)
            if chunk:
                pairs.append([query, chunk.text])
                valid.append(cand)

        if not pairs:
            return list(candidates)

        scores = self.model.predict(pairs)
        ranked = sorted(zip(valid, scores), key=lambda x: float(x[1]), reverse=True)

        max_score = float(ranked[0][1]) if ranked else 1.0
        reranked: list[CandidateRecord] = []
        for rank, (cand, score) in enumerate(ranked, start=1):
            reranked.append(
                replace(
                    cand,
                    rank=rank,
                    raw_score=float(score),
                    normalized_score=float(score) / max_score if max_score else 0.0,
                    retrieval_method=cand.retrieval_method + "+rerank",
                )
            )
        return reranked
