from __future__ import annotations

import json
import re
from pathlib import Path

from groundseal.models.chunk import ChunkRecord, make_chunk_id
from groundseal.models.document import DocumentRecord
from groundseal.models.source import SourceRecord
from groundseal.registry.store import SourceRegistry

CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
HEADING_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)

# strategy_name -> (chunk_size, overlap)
CHUNK_STRATEGIES: dict[str, tuple[int, int]] = {
    "baseline": (512, 64),
    "baseline-384": (384, 48),
    "baseline-512": (512, 64),
    "baseline-768": (768, 96),
}

STRATEGIES = frozenset(CHUNK_STRATEGIES.keys())


def strategy_params(strategy: str) -> tuple[int, int]:
    if strategy not in CHUNK_STRATEGIES:
        raise ValueError(f"Unknown chunk strategy: {strategy}. Choose from {sorted(STRATEGIES)}")
    return CHUNK_STRATEGIES[strategy]


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def split_sections(body: str) -> list[tuple[list[str], str]]:
    parts = HEADING_RE.split(body)
    if len(parts) == 1:
        return [([], body.strip())]

    sections: list[tuple[list[str], str]] = []
    preamble = parts[0].strip()
    if preamble:
        sections.append(([], preamble))

    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if content:
            sections.append(([heading], content))
    return sections


def window_chunks(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[tuple[int, int, str]]:
    if len(text) <= size:
        return [(0, len(text), text)]

    chunks: list[tuple[int, int, str]] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunk_text = text[start:end]
        chunks.append((start, end, chunk_text))
        if end >= len(text):
            break
        start = end - overlap
    return chunks


def resolve_chunk_permissions(
    source: SourceRecord,
    doc: DocumentRecord,
) -> tuple[str, list[str], list[str]]:
    visibility = source.visibility
    allowed_roles = list(source.allowed_roles)
    allowed_groups = list(source.allowed_groups)

    if doc.visibility_override:
        visibility = doc.visibility_override
    elif not doc.permission_inherit:
        visibility = doc.visibility_override or source.visibility

    return visibility, allowed_roles, allowed_groups


class BaselineChunker:
    def __init__(self, registry: SourceRegistry) -> None:
        self.registry = registry

    def chunk_document(
        self,
        document_id: str,
        source_id: str,
        body: str,
        source: SourceRecord,
        doc: DocumentRecord,
        base_offset: int = 0,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
    ) -> list[ChunkRecord]:
        visibility, allowed_roles, allowed_groups = resolve_chunk_permissions(source, doc)
        records: list[ChunkRecord] = []
        chunk_index = 0
        cursor = base_offset

        for heading_path, section_text in split_sections(body):
            for rel_start, rel_end, chunk_text in window_chunks(section_text, chunk_size, chunk_overlap):
                records.append(
                    ChunkRecord(
                        chunk_id=make_chunk_id(source_id, document_id, chunk_index),
                        document_id=document_id,
                        source_id=source_id,
                        text=chunk_text,
                        start_offset=cursor + rel_start,
                        end_offset=cursor + rel_end,
                        heading_path=heading_path,
                        chunk_index=chunk_index,
                        token_count=estimate_tokens(chunk_text),
                        visibility=visibility,
                        allowed_roles=allowed_roles,
                        allowed_groups=allowed_groups,
                        sensitivity=source.sensitivity,
                        citation_display_name=source.citation_display_name,
                        tenant_id=source.tenant_id,
                    )
                )
                chunk_index += 1
            cursor += len(section_text)

        return records

    def chunk_all(
        self,
        documents: list[DocumentRecord],
        get_body,
        strategy: str = "baseline",
    ) -> list[ChunkRecord]:
        chunk_size, chunk_overlap = strategy_params(strategy)

        all_chunks: list[ChunkRecord] = []
        for doc in documents:
            source = self.registry.get_source(doc.source_id)
            if source is None:
                continue
            body = get_body(doc)
            all_chunks.extend(
                self.chunk_document(
                    doc.document_id,
                    doc.source_id,
                    body,
                    source,
                    doc,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                )
            )
        return all_chunks

    def save_chunks(self, chunks: list[ChunkRecord], path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(json.dumps(chunk.to_dict()) + "\n")
        from groundseal.index.fingerprint import write_fingerprint, chunk_fingerprint

        write_fingerprint(path.with_suffix(".fingerprint.json"), chunk_fingerprint(chunks))

    def load_chunks(self, path: Path) -> list[ChunkRecord]:
        if not path.exists():
            return []
        chunks: list[ChunkRecord] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                chunks.append(ChunkRecord.from_dict(json.loads(line)))
        return chunks
