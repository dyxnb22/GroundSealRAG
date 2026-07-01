from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass
class SourceRecord:
    source_id: str
    title: str
    source_type: str
    uri: str
    owner_id: str
    tenant_id: str
    visibility: str
    allowed_roles: list[str]
    sensitivity: str
    freshness_updated_at: str
    registered_at: str
    citation_display_name: str
    allowed_groups: list[str] = field(default_factory=list)
    policy_tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SourceRecord:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
