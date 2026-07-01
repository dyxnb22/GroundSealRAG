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

    ingestor = MarkdownIngestor(registry, paths.root)
    result = ingestor.ingest_all(paths.sources_dir)
    assert len(result.documents) == 10
    for doc in result.documents:
        assert doc.source_id
        assert doc.document_id.startswith("DOC-")
        assert "body" not in doc.metadata


def test_ingest_detects_content_change(paths):
    registry = SourceRegistry(paths.registry_dir)
    registry.register_from_manifest(paths.manifest)
    ingestor = MarkdownIngestor(registry, paths.root)
    first = ingestor.ingest_all(paths.sources_dir)
    assert not first.changed_source_ids

    second = ingestor.ingest_all(paths.sources_dir)
    assert not second.changed_source_ids
    assert not second.needs_rechunk


def test_every_document_traces_to_source(paths):
    registry = SourceRegistry(paths.registry_dir)
    if not registry.list_sources():
        registry.register_from_manifest(paths.manifest)
    ingestor = MarkdownIngestor(registry, paths.root)
    if not registry.list_documents():
        ingestor.ingest_all(paths.sources_dir)

    for doc in registry.list_documents():
        source = registry.get_source(doc.source_id)
        assert source is not None
        body = ingestor.get_body(doc)
        assert len(body) > 100


def test_get_body_reads_from_file(paths, tmp_path):
    registry = SourceRegistry(paths.registry_dir)
    ingestor = MarkdownIngestor(registry, paths.root)
    registry.register_from_manifest(paths.manifest)
    result = ingestor.ingest_all(paths.sources_dir)
    doc = result.documents[0]
    body1 = ingestor.get_body(doc)
    assert body1
    assert not doc.metadata.get("body")
