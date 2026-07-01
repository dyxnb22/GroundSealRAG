from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from groundseal.chunking.baseline import BaselineChunker
from groundseal.freshness.filter import FreshnessFilter
from groundseal.index.fingerprint import chunk_fingerprint, is_fingerprint_current
from groundseal.ingestion.markdown_ingestor import MarkdownIngestor
from groundseal.paths import ProjectPaths
from groundseal.registry.store import SourceRegistry
from groundseal.retrieval.embeddings import EmbeddingModel, VectorIndex
from groundseal.retrieval.hybrid import HybridRetriever
from groundseal.retrieval.lexical import LexicalRetriever
from groundseal.retrieval.pipeline import RetrievalPipeline
from groundseal.retrieval.semantic import SemanticRetriever


def build_pipeline(paths: ProjectPaths, force_rebuild: bool = False) -> RetrievalPipeline:
    registry = SourceRegistry(paths.registry_dir)
    ingestor = MarkdownIngestor(registry, paths.root)

    if not registry.list_sources():
        registry.register_from_manifest(paths.manifest)

    documents = registry.list_documents()
    if not documents:
        ingestor.ingest_all(paths.sources_dir)
        documents = registry.list_documents()

    chunker = BaselineChunker(registry)
    fp_path = paths.chunks_path.with_suffix(".fingerprint.json")
    chunks = [] if force_rebuild else chunker.load_chunks(paths.chunks_path)

    if not chunks or force_rebuild:
        chunks = chunker.chunk_all(documents, ingestor.get_body)
        chunker.save_chunks(chunks, paths.chunks_path)
    elif not is_fingerprint_current(fp_path, chunk_fingerprint(chunks)):
        chunks = chunker.chunk_all(documents, ingestor.get_body)
        chunker.save_chunks(chunks, paths.chunks_path)

    lexical = LexicalRetriever(chunks, paths.bm25_dir)
    model = EmbeddingModel()

    if force_rebuild:
        vector_index = VectorIndex.build(chunks, model, paths.vectors_dir)
    else:
        vector_index = VectorIndex.load_or_build(chunks, model, paths.vectors_dir)

    semantic = SemanticRetriever(vector_index, model)
    hybrid = HybridRetriever(lexical, semantic)
    freshness = FreshnessFilter(registry)

    return RetrievalPipeline(
        chunks,
        lexical,
        semantic,
        hybrid,
        freshness_filter=freshness,
        reranker=None,
    )


@lru_cache(maxsize=4)
def _cached_pipeline(root: str, chunks_mtime: float, force_rebuild: bool) -> RetrievalPipeline:
    return build_pipeline(ProjectPaths(Path(root)), force_rebuild=force_rebuild)


def bootstrap(paths: ProjectPaths, force_rebuild: bool = False) -> RetrievalPipeline:
    """Build or return a cached pipeline keyed by project root and chunks mtime."""
    chunks_mtime = paths.chunks_path.stat().st_mtime if paths.chunks_path.exists() else 0.0
    return _cached_pipeline(str(paths.root.resolve()), chunks_mtime, force_rebuild)


def clear_pipeline_cache() -> None:
    _cached_pipeline.cache_clear()
