from __future__ import annotations

from groundseal.models.candidate import CandidateRecord
from groundseal.models.chunk import ChunkRecord

DEFAULT_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class CrossEncoderReranker:
    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import CrossEncoder

            self._model = CrossEncoder(self.model_name)
        return self._model

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
            return candidates

        scores = self.model.predict(pairs)
        ranked = sorted(zip(valid, scores), key=lambda x: float(x[1]), reverse=True)

        reranked: list[CandidateRecord] = []
        max_score = float(ranked[0][1]) if ranked else 1.0
        for rank, (cand, score) in enumerate(ranked, start=1):
            cand.rank = rank
            cand.raw_score = float(score)
            cand.normalized_score = float(score) / max_score if max_score else 0.0
            cand.retrieval_method = cand.retrieval_method + "+rerank"
            reranked.append(cand)
        return reranked
