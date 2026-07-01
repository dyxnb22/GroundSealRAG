from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from typing import Any


def make_chunk_id(source_id: str, document_id: str, chunk_index: int) -> str:
    raw = f"{source_id}:{document_id}:{chunk_index}"
    return "CHK-" + hashlib.sha256(raw.encode()).hexdigest()[:16]


@dataclass
class ChunkRecord:
    chunk_id: str
    document_id: str
    source_id: str
    text: str
    start_offset: int
    end_offset: int
    heading_path: list[str]
    chunk_index: int
    token_count: int
    visibility: str
    allowed_roles: list[str]
    sensitivity: str = "medium"
    citation_display_name: str = ""
    tenant_id: str = "tenant-default"
    allowed_groups: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ChunkRecord:
        known = cls.__dataclass_fields__
        filtered = {k: v for k, v in data.items() if k in known}
        if "allowed_groups" not in filtered:
            filtered["allowed_groups"] = []
        if "tenant_id" not in filtered:
            filtered["tenant_id"] = "tenant-default"
        return cls(**filtered)
