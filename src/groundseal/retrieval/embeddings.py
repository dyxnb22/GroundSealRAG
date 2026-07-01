from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from groundseal.models.chunk import ChunkRecord

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingModel:
    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
        return self._model

    def encode(self, texts: list[str]) -> np.ndarray:
        return np.array(self.model.encode(texts, normalize_embeddings=True))


class VectorIndex:
    def __init__(self, chunks: list[ChunkRecord], embeddings: np.ndarray, index_dir: Path | None = None) -> None:
        self.chunks = chunks
        self.embeddings = embeddings
        if index_dir:
            self.persist(index_dir)

    def persist(self, index_dir: Path) -> None:
        index_dir.mkdir(parents=True, exist_ok=True)
        np.save(index_dir / "embeddings.npy", self.embeddings)
        (index_dir / "chunk_ids.json").write_text(
            json.dumps([c.chunk_id for c in self.chunks]), encoding="utf-8"
        )

    @classmethod
    def load(cls, chunks: list[ChunkRecord], index_dir: Path) -> VectorIndex:
        embeddings = np.load(index_dir / "embeddings.npy")
        return cls(chunks, embeddings)

    @classmethod
    def build(cls, chunks: list[ChunkRecord], model: EmbeddingModel, index_dir: Path | None = None) -> VectorIndex:
        texts = [c.text for c in chunks]
        embeddings = model.encode(texts) if texts else np.zeros((0, 384))
        return cls(chunks, embeddings, index_dir)
