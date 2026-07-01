from __future__ import annotations

import hashlib

from groundseal.models.document import DocumentRecord
from groundseal.registry.store import SourceRegistry


def document_corpus_fingerprint(documents: list[DocumentRecord]) -> str:
    """Hash over all document content hashes for staleness detection."""
    payload = "|".join(f"{d.source_id}:{d.content_hash}" for d in sorted(documents, key=lambda d: d.source_id))
    return hashlib.sha256(payload.encode()).hexdigest()


def read_stored_corpus_fingerprint(registry: SourceRegistry) -> str | None:
    path = registry.registry_dir / "corpus_fingerprint.txt"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip() or None


def write_corpus_fingerprint(registry: SourceRegistry, fingerprint: str) -> None:
    path = registry.registry_dir / "corpus_fingerprint.txt"
    path.write_text(fingerprint + "\n", encoding="utf-8")


def corpus_is_stale(registry: SourceRegistry, documents: list[DocumentRecord]) -> bool:
    current = document_corpus_fingerprint(documents)
    stored = read_stored_corpus_fingerprint(registry)
    return stored != current
