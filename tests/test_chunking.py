import pytest

from groundseal.bootstrap import bootstrap
from groundseal.chunking.baseline import BaselineChunker
from groundseal.ingestion.markdown_ingestor import MarkdownIngestor
from groundseal.paths import ProjectPaths, find_project_root
from groundseal.registry.store import SourceRegistry


@pytest.fixture
def paths():
    return ProjectPaths(find_project_root())


def _prepare(paths):
    registry = SourceRegistry(paths.registry_dir)
    if not registry.list_sources():
        registry.register_from_manifest(paths.manifest)
    ingestor = MarkdownIngestor(registry, paths.root)
    if not registry.list_documents():
        ingestor.ingest_all(paths.sources_dir)
    return registry, ingestor


def test_chunking_produces_stable_ids(paths):
    registry, ingestor = _prepare(paths)
    chunker = BaselineChunker(registry)
    documents = registry.list_documents()
    chunks = chunker.chunk_all(documents, ingestor.get_body)
    assert 100 <= len(chunks) <= 280
    for c in chunks:
        assert c.source_id
        assert c.document_id
        assert c.chunk_id.startswith("CHK-")
        assert c.tenant_id


def test_chunk_01_boundary_inspectable(paths):
    registry, ingestor = _prepare(paths)
    chunker = BaselineChunker(registry)
    documents = registry.list_documents()
    chunks = chunker.chunk_all(documents, ingestor.get_body)
    assert any(c.heading_path for c in chunks)
    assert all(c.end_offset >= c.start_offset for c in chunks)
