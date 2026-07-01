from __future__ import annotations

from groundseal.chunking.baseline import BaselineChunker
from groundseal.freshness.filter import FreshnessFilter
from groundseal.index.corpus_fingerprint import (
    corpus_is_stale,
    document_corpus_fingerprint,
    write_corpus_fingerprint,
)
from groundseal.index.fingerprint import chunk_fingerprint, is_fingerprint_current
from groundseal.ingestion.markdown_ingestor import MarkdownIngestor
from groundseal.paths import ProjectPaths
from groundseal.registry.store import SourceRegistry
from groundseal.retrieval.embeddings import EmbeddingModel, VectorIndex
from groundseal.retrieval.hybrid import HybridRetriever
from groundseal.retrieval.lexical import LexicalRetriever
from groundseal.retrieval.pipeline import RetrievalPipeline
from groundseal.retrieval.semantic import SemanticRetriever


def rebuild_chunks(paths: ProjectPaths, strategy: str = "baseline") -> int:
    registry = SourceRegistry(paths.registry_dir)
    ingestor = MarkdownIngestor(registry, paths.root)
    documents = registry.list_documents()
    if not documents:
        raise ValueError("No documents ingested. Run: groundseal ingest --all")

    chunker = BaselineChunker(registry)
    chunks = chunker.chunk_all(documents, ingestor.get_body, strategy=strategy)
    chunker.save_chunks(chunks, paths.chunks_path)
    write_corpus_fingerprint(registry, document_corpus_fingerprint(documents))
    return len(chunks)


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

    stale_corpus = corpus_is_stale(registry, documents)
    stale_chunks = chunks and not is_fingerprint_current(fp_path, chunk_fingerprint(chunks))

    if not chunks or force_rebuild or stale_corpus or stale_chunks:
        chunks = chunker.chunk_all(documents, ingestor.get_body)
        chunker.save_chunks(chunks, paths.chunks_path)
        write_corpus_fingerprint(registry, document_corpus_fingerprint(documents))

    lexical = LexicalRetriever(chunks, paths.bm25_dir)
    model = EmbeddingModel()

    if force_rebuild or stale_corpus or stale_chunks:
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


# Re-export bootstrap helpers from bootstrap module to avoid circular imports in CLI
__all__ = ["build_pipeline", "rebuild_chunks"]
