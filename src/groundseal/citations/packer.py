from __future__ import annotations

import uuid

from groundseal.models.candidate import CandidateRecord
from groundseal.models.chunk import ChunkRecord
from groundseal.models.citation import CitationItem, CitationPackage
from groundseal.models.source import utc_now_iso

DEFAULT_BUDGET_TOKENS = 2048


class CitationPacker:
    def __init__(self, budget_tokens: int = DEFAULT_BUDGET_TOKENS) -> None:
        self.budget_tokens = budget_tokens

    def pack(
        self,
        query: str,
        requester_id: str,
        candidates: list[CandidateRecord],
        chunk_map: dict[str, ChunkRecord],
        permission_decisions: dict[str, str],
    ) -> CitationPackage:
        citations: list[CitationItem] = []
        excluded: list[str] = []
        used_tokens = 0
        seen_sources: set[str] = set()

        for cand in candidates:
            chunk = chunk_map.get(cand.chunk_id)
            if chunk is None:
                excluded.append(cand.chunk_id)
                continue

            perm = permission_decisions.get(cand.chunk_id, "deny")
            if perm != "allow":
                excluded.append(cand.chunk_id)
                continue

            tokens = chunk.token_count
            if used_tokens + tokens > self.budget_tokens:
                excluded.append(cand.chunk_id)
                continue

            # prefer diversity: skip redundant same-source if we already have 2 from it
            source_count = sum(1 for c in citations if c.source_id == chunk.source_id)
            if source_count >= 2 and chunk.source_id in seen_sources:
                excluded.append(cand.chunk_id)
                continue

            label = chunk.citation_display_name
            if chunk.heading_path:
                label = f"{label} > {' > '.join(chunk.heading_path)}"

            citations.append(
                CitationItem(
                    citation_id=f"CITE-{uuid.uuid4().hex[:8]}",
                    chunk_id=chunk.chunk_id,
                    source_id=chunk.source_id,
                    document_id=chunk.document_id,
                    label=label,
                    excerpt=chunk.text[:500],
                    rank=len(citations) + 1,
                    permission_decision="allow",
                )
            )
            used_tokens += tokens
            seen_sources.add(chunk.source_id)

        return CitationPackage(
            package_id=f"PKG-{uuid.uuid4().hex[:8]}",
            query=query,
            requester_id=requester_id,
            citations=citations,
            excluded=excluded,
            budget_tokens=self.budget_tokens,
            assembled_at=utc_now_iso(),
        )
