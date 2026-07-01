from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class EvalCase:
    case_id: str
    query: str
    requester_id: str
    expected_source_ids: list[str] = field(default_factory=list)
    expected_chunk_ids: list[str] = field(default_factory=list)
    expected_inaccessible: bool = False
    method: str = "hybrid"
    top_k: int = 5
    notes: str = ""
    category: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EvalCase:
        return cls(
            case_id=data["case_id"],
            query=data["query"],
            requester_id=data["requester_id"],
            expected_source_ids=data.get("expected_source_ids", []),
            expected_chunk_ids=data.get("expected_chunk_ids", []),
            expected_inaccessible=data.get("expected_inaccessible", False),
            method=data.get("method", "hybrid"),
            top_k=data.get("top_k", 5),
            notes=data.get("notes", ""),
            category=data.get("category", ""),
        )


def load_cases(cases_dir: Path) -> list[EvalCase]:
    cases: list[EvalCase] = []
    for path in sorted(cases_dir.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            cases.extend(EvalCase.from_dict(c) for c in data)
        else:
            cases.append(EvalCase.from_dict(data))
    return cases
