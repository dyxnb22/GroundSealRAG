"""Index staleness detection for retrieval caches."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from groundseal.models.chunk import ChunkRecord


def chunk_fingerprint(chunks: list[ChunkRecord]) -> str:
    """Stable hash over ordered chunk IDs."""
    payload = "|".join(c.chunk_id for c in chunks)
    return hashlib.sha256(payload.encode()).hexdigest()


def document_fingerprint(doc_hashes: list[str]) -> str:
    payload = "|".join(sorted(doc_hashes))
    return hashlib.sha256(payload.encode()).hexdigest()


def write_fingerprint(path: Path, fingerprint: str, extra: dict | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"fingerprint": fingerprint, **(extra or {})}
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.replace(path)


def read_fingerprint(path: Path) -> str | None:
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("fingerprint")


def is_fingerprint_current(path: Path, expected: str) -> bool:
    stored = read_fingerprint(path)
    return stored == expected
