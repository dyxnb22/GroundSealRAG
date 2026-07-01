from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class PermissionDecision:
    chunk_id: str
    requester_id: str
    decision: str  # allow | deny
    reason_code: str
    matched_rule: str
    evaluated_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PermissionDecision:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
