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
    def __init__(self, registry: SourceRegistry, project_root: Path) -> None:
        self.registry = registry
        self.project_root = project_root

    def resolve_path(self, content_path: str) -> Path:
        path = Path(content_path)
        if path.is_absolute():
            return path
        return self.project_root / content_path

    def ingest_file(self, path: Path, source_id: str | None = None) -> DocumentRecord:
        meta, body = parse_markdown(path)
        sid = source_id or meta.get("source_id")
        if not sid:
            raise ValueError(f"source_id required for {path}")

        source = self.registry.get_source(sid)
        if source is None:
            raise ValueError(f"Source not registered: {sid}")

        try:
            rel_path = str(path.relative_to(self.project_root))
        except ValueError:
            rel_path = str(path)

        doc = DocumentRecord(
            document_id=f"DOC-{sid}",
            source_id=sid,
            title=meta.get("title", source.title),
            format="markdown",
            content_hash=content_hash(body),
            content_path=rel_path,
            ingested_at=utc_now_iso(),
            byte_size=path.stat().st_size,
            permission_inherit=True,
            metadata={},
        )
        self.registry.add_document(doc)
        return doc

    def ingest_all(self, sources_dir: Path) -> list[DocumentRecord]:
        docs: list[DocumentRecord] = []
        for path in sorted(sources_dir.glob("*.md")):
            meta, _ = parse_markdown(path)
            docs.append(self.ingest_file(path, meta.get("source_id")))
        return docs

    def get_body(self, doc: DocumentRecord) -> str:
        path = self.resolve_path(doc.content_path)
        if not path.exists():
            raise FileNotFoundError(f"Document content not found: {path}")
        _, body = parse_markdown(path)
        return body

    def content_changed(self, doc: DocumentRecord) -> bool:
        return content_hash(self.get_body(doc)) != doc.content_hash
