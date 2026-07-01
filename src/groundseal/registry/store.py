from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

import yaml

from groundseal.models.document import DocumentRecord
from groundseal.models.source import SourceRecord, utc_now_iso


class RegistryError(Exception):
    """Raised when registry operations fail validation."""


class SourceRegistry:
    def __init__(self, registry_dir: Path) -> None:
        self.registry_dir = registry_dir
        self.sources_path = registry_dir / "sources.json"
        self.documents_path = registry_dir / "documents.json"
        self.registry_dir.mkdir(parents=True, exist_ok=True)

    def _load_json(self, path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    def _save_json(self, path: Path, data: list[dict[str, Any]]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(tmp_path, path)
        except Exception:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise

    def list_sources(self) -> list[SourceRecord]:
        return [SourceRecord.from_dict(s) for s in self._load_json(self.sources_path)]

    def get_source(self, source_id: str) -> SourceRecord | None:
        for s in self.list_sources():
            if s.source_id == source_id:
                return s
        return None

    def register_source(self, source: SourceRecord) -> None:
        sources = self._load_json(self.sources_path)
        sources = [s for s in sources if s["source_id"] != source.source_id]
        sources.append(source.to_dict())
        self._save_json(self.sources_path, sources)

    def register_from_manifest(self, manifest_path: Path) -> list[SourceRecord]:
        raw = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        if not raw or "sources" not in raw:
            raise RegistryError(f"Invalid manifest: missing 'sources' in {manifest_path}")

        registered: list[SourceRecord] = []
        required = ("source_id", "title", "uri", "owner_id", "visibility", "allowed_roles")
        for entry in raw["sources"]:
            missing = [f for f in required if f not in entry]
            if missing:
                raise RegistryError(f"Manifest entry missing fields {missing}: {entry.get('source_id', '?')}")
            source = SourceRecord(
                source_id=entry["source_id"],
                title=entry["title"],
                source_type=entry.get("source_type", "markdown"),
                uri=entry["uri"],
                owner_id=entry["owner_id"],
                tenant_id=entry.get("tenant_id", "tenant-default"),
                visibility=entry["visibility"],
                allowed_roles=entry["allowed_roles"],
                allowed_groups=entry.get("allowed_groups", []),
                sensitivity=entry.get("sensitivity", "medium"),
                policy_tags=entry.get("policy_tags", []),
                freshness_updated_at=entry.get("freshness_updated_at", utc_now_iso()),
                registered_at=utc_now_iso(),
                citation_display_name=entry.get("citation_display_name", entry["title"]),
            )
            self.register_source(source)
            registered.append(source)
        return registered

    def list_documents(self) -> list[DocumentRecord]:
        return [DocumentRecord.from_dict(d) for d in self._load_json(self.documents_path)]

    def save_documents(self, documents: list[DocumentRecord]) -> None:
        self._save_json(self.documents_path, [d.to_dict() for d in documents])

    def add_document(self, doc: DocumentRecord) -> None:
        docs = self.list_documents()
        docs = [d for d in docs if d.document_id != doc.document_id]
        docs.append(doc)
        self.save_documents(docs)

    def document_hashes(self) -> list[str]:
        return [d.content_hash for d in self.list_documents()]
