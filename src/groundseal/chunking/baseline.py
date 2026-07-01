from __future__ import annotations

import json
import re
from pathlib import Path

from groundseal.models.chunk import ChunkRecord, make_chunk_id
from groundseal.models.source import SourceRecord
from groundseal.registry.store import SourceRegistry

CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
HEADING_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)


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


class BaselineChunker:
    def __init__(self, registry: SourceRegistry) -> None:
        self.registry = registry

    def chunk_document(
        self,
        document_id: str,
        source_id: str,
        body: str,
        source: SourceRecord,
        base_offset: int = 0,
    ) -> list[ChunkRecord]:
        records: list[ChunkRecord] = []
        chunk_index = 0
        cursor = base_offset

        for heading_path, section_text in split_sections(body):
            for rel_start, rel_end, chunk_text in window_chunks(section_text):
                abs_start = cursor + rel_start
                abs_end = cursor + rel_end
                chunk_id = make_chunk_id(source_id, document_id, chunk_index)
                records.append(
                    ChunkRecord(
                        chunk_id=chunk_id,
                        document_id=document_id,
                        source_id=source_id,
                        text=chunk_text,
                        start_offset=abs_start,
                        end_offset=abs_end,
                        heading_path=heading_path,
                        chunk_index=chunk_index,
                        token_count=estimate_tokens(chunk_text),
                        visibility=source.visibility,
                        allowed_roles=list(source.allowed_roles),
                        sensitivity=source.sensitivity,
                        citation_display_name=source.citation_display_name,
                    )
                )
                chunk_index += 1
            cursor += len(section_text) + 1

        return records

    def chunk_all(self, documents: list[dict], get_body) -> list[ChunkRecord]:
        all_chunks: list[ChunkRecord] = []
        for doc_dict in documents:
            from groundseal.models.document import DocumentRecord

            doc = DocumentRecord.from_dict(doc_dict)
            source = self.registry.get_source(doc.source_id)
            if source is None:
                continue
            body = get_body(doc)
            all_chunks.extend(self.chunk_document(doc.document_id, doc.source_id, body, source))
        return all_chunks

    def save_chunks(self, chunks: list[ChunkRecord], path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(json.dumps(chunk.to_dict()) + "\n")

    def load_chunks(self, path: Path) -> list[ChunkRecord]:
        if not path.exists():
            return []
        chunks: list[ChunkRecord] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                chunks.append(ChunkRecord.from_dict(json.loads(line)))
        return chunks
