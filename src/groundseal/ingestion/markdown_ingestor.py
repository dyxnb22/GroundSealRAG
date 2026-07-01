from __future__ import annotations

import hashlib
import re
from pathlib import Path

import yaml

from groundseal.models.document import DocumentRecord
from groundseal.models.source import utc_now_iso
from groundseal.registry.store import SourceRegistry


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_markdown(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"Missing YAML frontmatter: {path}")
    meta = yaml.safe_load(match.group(1)) or {}
    body = text[match.end() :].strip()
    return meta, body


def content_hash(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


class MarkdownIngestor:
    def __init__(self, registry: SourceRegistry, corpus_root: Path) -> None:
        self.registry = registry
        self.corpus_root = corpus_root

    def ingest_file(self, path: Path, source_id: str | None = None) -> DocumentRecord:
        meta, body = parse_markdown(path)
        sid = source_id or meta.get("source_id")
        if not sid:
            raise ValueError(f"source_id required for {path}")

        source = self.registry.get_source(sid)
        if source is None:
            raise ValueError(f"Source not registered: {sid}")

        doc = DocumentRecord(
            document_id=f"DOC-{sid}",
            source_id=sid,
            title=meta.get("title", source.title),
            format="markdown",
            content_hash=content_hash(body),
            content_path=str(path.relative_to(self.corpus_root.parent) if path.is_relative_to(self.corpus_root.parent) else path),
            ingested_at=utc_now_iso(),
            byte_size=path.stat().st_size,
            permission_inherit=True,
            metadata={"body": body},
        )
        self.registry.add_document(doc.to_dict())
        return doc

    def ingest_all(self, sources_dir: Path) -> list[DocumentRecord]:
        docs: list[DocumentRecord] = []
        for path in sorted(sources_dir.glob("*.md")):
            meta, _ = parse_markdown(path)
            docs.append(self.ingest_file(path, meta.get("source_id")))
        return docs

    def get_body(self, doc: DocumentRecord) -> str:
        if "body" in doc.metadata:
            return doc.metadata["body"]
        path = self.corpus_root.parent / doc.content_path
        _, body = parse_markdown(path)
        return body
