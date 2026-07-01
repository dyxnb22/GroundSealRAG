from __future__ import annotations

import json
import re
import uuid
from pathlib import Path

from rank_bm25 import BM25Okapi

from groundseal.models.candidate import CandidateRecord
from groundseal.models.chunk import ChunkRecord
from groundseal.models.source import utc_now_iso

TOKEN_RE = re.compile(r"\w+")


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]


class LexicalRetriever:
    def __init__(self, chunks: list[ChunkRecord], index_dir: Path | None = None) -> None:
        self.chunks = chunks
        self.index_dir = index_dir
        self.corpus_tokens = [tokenize(c.text) for c in chunks]
        self.bm25 = BM25Okapi(self.corpus_tokens) if self.corpus_tokens else None
        if index_dir:
            self._persist(index_dir)

    def _persist(self, index_dir: Path) -> None:
        index_dir.mkdir(parents=True, exist_ok=True)
        meta = {"chunk_ids": [c.chunk_id for c in self.chunks]}
        (index_dir / "meta.json").write_text(json.dumps(meta), encoding="utf-8")

    @classmethod
    def load(cls, chunks: list[ChunkRecord], index_dir: Path) -> LexicalRetriever:
        return cls(chunks, index_dir)

    def search(self, query: str, top_k: int = 10, query_id: str | None = None) -> list[CandidateRecord]:
        if not self.bm25 or not self.chunks:
            return []

        qid = query_id or str(uuid.uuid4())
        tokens = tokenize(query)
        scores = self.bm25.get_scores(tokens)
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]

        max_score = max((s for _, s in ranked), default=1.0) or 1.0
        candidates: list[CandidateRecord] = []
        for rank, (idx, raw_score) in enumerate(ranked, start=1):
            chunk = self.chunks[idx]
            if raw_score <= 0:
                continue
            candidates.append(
                CandidateRecord(
                    candidate_id=f"CAND-lex-{uuid.uuid4().hex[:8]}",
                    query_id=qid,
                    chunk_id=chunk.chunk_id,
                    source_id=chunk.source_id,
                    document_id=chunk.document_id,
                    retrieval_method="lexical",
                    raw_score=float(raw_score),
                    normalized_score=float(raw_score / max_score),
                    rank=rank,
                    retrieved_at=utc_now_iso(),
                    query_text=query,
                )
            )
        return candidates
