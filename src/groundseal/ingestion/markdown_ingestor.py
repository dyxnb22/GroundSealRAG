from __future__ import annotations

import hashlib
import re
from pathlib import Path

import yaml

from groundseal.models.document import DocumentRecord
from groundseal.models.source import utc_now_iso
from groundseal.ingestion.result import IngestResult
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
    def __init__(self, registry: SourceRegistry, project_root: Path) -> None:
        self.registry = registry
        self.project_root = project_root

    def resolve_path(self, content_path: str) -> Path:
        path = Path(content_path)
        if path.is_absolute():
            return path
        return self.project_root / content_path

    def _existing_document(self, source_id: str) -> DocumentRecord | None:
        for doc in self.registry.list_documents():
            if doc.source_id == source_id:
                return doc
        return None

    def ingest_file(self, path: Path, source_id: str | None = None) -> tuple[DocumentRecord, bool, bool]:
        """Returns (document, content_changed, is_new)."""
        meta, body = parse_markdown(path)
        sid = source_id or meta.get("source_id")
        if not sid:
            raise ValueError(f"source_id required for {path}")

        source = self.registry.get_source(sid)
        if source is None:
            raise ValueError(f"Source not registered: {sid}")

        existing = self._existing_document(sid)
        new_hash = content_hash(body)
        is_new = existing is None
        content_changed = is_new or existing.content_hash != new_hash

        try:
            rel_path = str(path.relative_to(self.project_root))
        except ValueError:
            rel_path = str(path)

        doc = DocumentRecord(
            document_id=f"DOC-{sid}",
            source_id=sid,
            title=meta.get("title", source.title),
            format="markdown",
            content_hash=new_hash,
            content_path=rel_path,
            ingested_at=utc_now_iso(),
            byte_size=path.stat().st_size,
            permission_inherit=True,
            metadata={},
        )
        self.registry.add_document(doc)
        return doc, content_changed, is_new

    def ingest_all(self, sources_dir: Path) -> IngestResult:
        documents: list[DocumentRecord] = []
        changed: list[str] = []
        new_ids: list[str] = []
        for path in sorted(sources_dir.glob("*.md")):
            meta, _ = parse_markdown(path)
            doc, content_changed, is_new = self.ingest_file(path, meta.get("source_id"))
            documents.append(doc)
            if is_new:
                new_ids.append(doc.source_id)
            elif content_changed:
                changed.append(doc.source_id)
        return IngestResult(documents=documents, changed_source_ids=changed, new_source_ids=new_ids)

    def get_body(self, doc: DocumentRecord) -> str:
        path = self.resolve_path(doc.content_path)
        if not path.exists():
            raise FileNotFoundError(f"Document content not found: {path}")
        _, body = parse_markdown(path)
        return body

    def content_changed(self, doc: DocumentRecord) -> bool:
        return content_hash(self.get_body(doc)) != doc.content_hash
