from __future__ import annotations

from dataclasses import dataclass, field

from groundseal.models.document import DocumentRecord


@dataclass
class IngestResult:
    documents: list[DocumentRecord]
    changed_source_ids: list[str] = field(default_factory=list)
    new_source_ids: list[str] = field(default_factory=list)

    @property
    def needs_rechunk(self) -> bool:
        return bool(self.changed_source_ids or self.new_source_ids)
