from __future__ import annotations

from datetime import datetime, timezone

from groundseal.models.chunk import ChunkRecord
from groundseal.registry.store import SourceRegistry

STALE_DAYS = 90


def parse_iso(ts: str) -> datetime:
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)


class FreshnessFilter:
    def __init__(self, registry: SourceRegistry, stale_days: int = STALE_DAYS) -> None:
        self.registry = registry
        self.stale_days = stale_days

    def is_stale(self, source_id: str) -> bool:
        source = self.registry.get_source(source_id)
        if source is None or not source.freshness_updated_at:
            return True
        updated = parse_iso(source.freshness_updated_at)
        now = datetime.now(timezone.utc)
        age_days = (now - updated).days
        return age_days > self.stale_days

    def filter_chunks(self, chunks: list[ChunkRecord], exclude_stale: bool = True) -> list[ChunkRecord]:
        if not exclude_stale:
            return chunks
        return [c for c in chunks if not self.is_stale(c.source_id)]

    def downrank_score(self, source_id: str, score: float) -> float:
        if self.is_stale(source_id):
            return score * 0.5
        return score
