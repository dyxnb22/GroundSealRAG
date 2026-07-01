from __future__ import annotations

from groundseal.chunking.baseline import BaselineChunker
from groundseal.ingestion.markdown_ingestor import MarkdownIngestor
from groundseal.paths import ProjectPaths
from groundseal.registry.store import SourceRegistry
from groundseal.retrieval.embeddings import EmbeddingModel, VectorIndex
from groundseal.retrieval.hybrid import HybridRetriever
from groundseal.retrieval.lexical import LexicalRetriever
from groundseal.retrieval.pipeline import RetrievalPipeline
from groundseal.retrieval.rerank import CrossEncoderReranker
from groundseal.retrieval.semantic import SemanticRetriever


def bootstrap(paths: ProjectPaths, build_embeddings: bool = True) -> RetrievalPipeline:
    registry = SourceRegistry(paths.registry_dir)
    ingestor = MarkdownIngestor(registry, paths.corpus)

    if not registry.list_sources():
        registry.register_from_manifest(paths.manifest)

    docs = registry.list_documents()
    if not docs:
        ingestor.ingest_all(paths.sources_dir)
        docs = registry.list_documents()

    chunker = BaselineChunker(registry)
    chunks = chunker.load_chunks(paths.chunks_path)
    if not chunks:
        chunks = chunker.chunk_all(docs, lambda doc: ingestor.get_body(doc))
        chunker.save_chunks(chunks, paths.chunks_path)

    lexical = LexicalRetriever(chunks, paths.bm25_dir)
    model = EmbeddingModel()
    if build_embeddings and not (paths.vectors_dir / "embeddings.npy").exists():
        vector_index = VectorIndex.build(chunks, model, paths.vectors_dir)
    else:
        vector_index = VectorIndex.load(chunks, paths.vectors_dir) if (paths.vectors_dir / "embeddings.npy").exists() else VectorIndex.build(chunks, model, paths.vectors_dir)

    semantic = SemanticRetriever(vector_index, model)
    hybrid = HybridRetriever(lexical, semantic)
    reranker = CrossEncoderReranker()

    return RetrievalPipeline(chunks, lexical, semantic, hybrid, reranker=reranker)
