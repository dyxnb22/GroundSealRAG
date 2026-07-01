from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class CitationItem:
    citation_id: str
    chunk_id: str
    source_id: str
    document_id: str
    label: str
    excerpt: str
    rank: int
    permission_decision: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CitationPackage:
    package_id: str
    query: str
    requester_id: str
    citations: list[CitationItem]
    excluded: list[str]
    budget_tokens: int
    assembled_at: str

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["citations"] = [c.to_dict() if isinstance(c, CitationItem) else c for c in self.citations]
        return d
