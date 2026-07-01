from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class CandidateRecord:
    candidate_id: str
    query_id: str
    chunk_id: str
    source_id: str
    document_id: str
    retrieval_method: str
    raw_score: float
    normalized_score: float
    rank: int
    retrieved_at: str
    query_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CandidateRecord:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
