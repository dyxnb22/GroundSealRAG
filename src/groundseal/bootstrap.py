from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from groundseal.paths import ProjectPaths
from groundseal.pipeline.build import build_pipeline as _build_pipeline
from groundseal.pipeline.build import rebuild_chunks


@lru_cache(maxsize=4)
def _cached_pipeline(root: str, chunks_mtime: float, force_rebuild: bool):
    return _build_pipeline(ProjectPaths(Path(root)), force_rebuild=force_rebuild)


def bootstrap(paths: ProjectPaths, force_rebuild: bool = False):
    """Build or return a cached pipeline keyed by project root and chunks mtime."""
    chunks_mtime = paths.chunks_path.stat().st_mtime if paths.chunks_path.exists() else 0.0
    return _cached_pipeline(str(paths.root.resolve()), chunks_mtime, force_rebuild)


def clear_pipeline_cache() -> None:
    _cached_pipeline.cache_clear()


__all__ = ["bootstrap", "clear_pipeline_cache", "rebuild_chunks"]
