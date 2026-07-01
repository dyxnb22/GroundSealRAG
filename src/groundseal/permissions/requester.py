from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from groundseal.permissions.constants import VISIBILITY_ORDER  # noqa: F401 — re-export


@dataclass
class RequesterContext:
    requester_id: str
    roles: list[str] = field(default_factory=list)
    allowed_visibilities: list[str] = field(default_factory=list)
    allowed_source_ids: list[str] | None = None
    tenant_id: str = "tenant-default"

    @classmethod
    def from_yaml(cls, path: Path) -> RequesterContext:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not data or "requester_id" not in data:
            raise ValueError(f"Invalid persona file: {path}")
        return cls(
            requester_id=data["requester_id"],
            roles=data.get("roles", []),
            allowed_visibilities=data.get("allowed_visibilities", []),
            allowed_source_ids=data.get("allowed_source_ids"),
            tenant_id=data.get("tenant_id", "tenant-default"),
        )


def load_requester(personas_dir: Path, requester_id: str) -> RequesterContext:
    path = personas_dir / f"{requester_id}.yaml"
    if not path.exists():
        raise ValueError(f"Unknown requester: {requester_id}")
    return RequesterContext.from_yaml(path)
