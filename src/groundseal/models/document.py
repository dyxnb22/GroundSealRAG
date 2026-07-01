from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class DocumentRecord:
    document_id: str
    source_id: str
    title: str
    format: str
    content_hash: str
    content_path: str
    ingested_at: str
    byte_size: int
    permission_inherit: bool = True
    visibility_override: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DocumentRecord:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
