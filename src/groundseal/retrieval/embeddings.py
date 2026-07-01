from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from groundseal.index.fingerprint import chunk_fingerprint, is_fingerprint_current, write_fingerprint
from groundseal.models.chunk import ChunkRecord

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Module-level singleton avoids reloading the model per CLI invocation.
_MODEL_CACHE: dict[str, object] = {}


class EmbeddingModel:
    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        self.model_name = model_name

    @property
    def model(self):
        if self.model_name not in _MODEL_CACHE:
            from sentence_transformers import SentenceTransformer

            _MODEL_CACHE[self.model_name] = SentenceTransformer(self.model_name)
        return _MODEL_CACHE[self.model_name]

    def encode(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, self.embedding_dim), dtype=np.float32)
        return np.array(self.model.encode(texts, normalize_embeddings=True), dtype=np.float32)

    @property
    def embedding_dim(self) -> int:
        return int(self.model.get_sentence_embedding_dimension())


class VectorIndex:
    def __init__(
        self,
        chunks: list[ChunkRecord],
        embeddings: np.ndarray,
        index_dir: Path | None = None,
        model_name: str = DEFAULT_MODEL,
    ) -> None:
        if embeddings.shape[0] != len(chunks):
            raise ValueError(
                f"Embedding rows ({embeddings.shape[0]}) must match chunk count ({len(chunks)})"
            )
        self.chunks = chunks
        self.embeddings = embeddings
        self.model_name = model_name
        if index_dir:
            self.persist(index_dir)

    def persist(self, index_dir: Path) -> None:
        index_dir.mkdir(parents=True, exist_ok=True)
        np.save(index_dir / "embeddings.npy", self.embeddings)
        (index_dir / "chunk_ids.json").write_text(
            json.dumps([c.chunk_id for c in self.chunks]), encoding="utf-8"
        )
        write_fingerprint(
            index_dir / "fingerprint.json",
            chunk_fingerprint(self.chunks),
            extra={"model": self.model_name, "count": len(self.chunks)},
        )

    @classmethod
    def load(cls, chunks: list[ChunkRecord], index_dir: Path, model_name: str = DEFAULT_MODEL) -> VectorIndex:
        embeddings_path = index_dir / "embeddings.npy"
        chunk_ids_path = index_dir / "chunk_ids.json"
        if not embeddings_path.exists() or not chunk_ids_path.exists():
            raise FileNotFoundError(f"Vector index incomplete in {index_dir}")

        stored_ids: list[str] = json.loads(chunk_ids_path.read_text(encoding="utf-8"))
        current_ids = [c.chunk_id for c in chunks]
        if stored_ids != current_ids:
            raise ValueError("Vector index chunk_ids do not match current chunks; rebuild required")

        if not is_fingerprint_current(index_dir / "fingerprint.json", chunk_fingerprint(chunks)):
            raise ValueError("Vector index fingerprint stale; rebuild required")

        embeddings = np.load(embeddings_path)
        return cls(chunks, embeddings, model_name=model_name)

    @classmethod
    def build(
        cls,
        chunks: list[ChunkRecord],
        model: EmbeddingModel,
        index_dir: Path | None = None,
    ) -> VectorIndex:
        texts = [c.text for c in chunks]
        embeddings = model.encode(texts)
        return cls(chunks, embeddings, index_dir, model_name=model.model_name)

    @classmethod
    def load_or_build(
        cls,
        chunks: list[ChunkRecord],
        model: EmbeddingModel,
        index_dir: Path,
    ) -> VectorIndex:
        try:
            return cls.load(chunks, index_dir, model_name=model.model_name)
        except (FileNotFoundError, ValueError):
            return cls.build(chunks, model, index_dir)
