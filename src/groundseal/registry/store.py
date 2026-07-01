from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from groundseal.models.source import SourceRecord, utc_now_iso


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
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

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
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        registered: list[SourceRecord] = []
        for entry in manifest.get("sources", []):
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

    def list_documents(self) -> list[dict[str, Any]]:
        return self._load_json(self.documents_path)

    def save_documents(self, documents: list[dict[str, Any]]) -> None:
        self._save_json(self.documents_path, documents)

    def add_document(self, doc: dict[str, Any]) -> None:
        docs = self.list_documents()
        docs = [d for d in docs if d["document_id"] != doc["document_id"]]
        docs.append(doc)
        self.save_documents(docs)
