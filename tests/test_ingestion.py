import pytest
from pathlib import Path

from groundseal.paths import ProjectPaths, find_project_root
from groundseal.registry.store import SourceRegistry
from groundseal.ingestion.markdown_ingestor import MarkdownIngestor


@pytest.fixture
def paths():
    return ProjectPaths(find_project_root())


def test_register_and_ingest_all(paths):
    registry = SourceRegistry(paths.registry_dir)
    registry.register_from_manifest(paths.manifest)
    sources = registry.list_sources()
    assert len(sources) == 10

    ingestor = MarkdownIngestor(registry, paths.corpus)
    docs = ingestor.ingest_all(paths.sources_dir)
    assert len(docs) == 10
    for doc in docs:
        assert doc.source_id
        assert doc.document_id.startswith("DOC-")


def test_every_document_traces_to_source(paths):
    registry = SourceRegistry(paths.registry_dir)
    if not registry.list_sources():
        registry.register_from_manifest(paths.manifest)
    ingestor = MarkdownIngestor(registry, paths.corpus)
    if not registry.list_documents():
        ingestor.ingest_all(paths.sources_dir)

    for doc in registry.list_documents():
        source = registry.get_source(doc["source_id"])
        assert source is not None
