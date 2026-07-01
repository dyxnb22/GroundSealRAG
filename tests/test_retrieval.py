import pytest

from groundseal.bootstrap import bootstrap, clear_pipeline_cache
from groundseal.paths import ProjectPaths, find_project_root
from groundseal.permissions.requester import RequesterContext, load_requester


@pytest.fixture
def paths():
    return ProjectPaths(find_project_root())


@pytest.fixture
def pipeline(paths):
    clear_pipeline_cache()
    return bootstrap(paths)


def test_lexical_retrieval(pipeline, paths):
    req = load_requester(paths.personas_dir, "admin_full")
    result = pipeline.retrieve("API token rotation", req, method="lexical", top_k=5)
    assert result.allowed_candidates
    sources = {c.source_id for c in result.allowed_candidates}
    assert "SRC-api-auth" in sources


def test_permission_blocks_confidential(pipeline, paths):
    req = load_requester(paths.personas_dir, "engineer_std")
    result = pipeline.retrieve(
        "data encryption at rest requirements", req, method="hybrid", top_k=10
    )
    allowed_sources = {c.source_id for c in result.allowed_candidates}
    assert "SRC-security-policy" not in allowed_sources


def test_guest_gets_no_results(pipeline, paths):
    req = load_requester(paths.personas_dir, "guest_none")
    result = pipeline.retrieve("remote work guidelines", req, method="hybrid", top_k=5)
    assert not result.allowed_candidates


def test_invalid_method_raises(pipeline, paths):
    req = load_requester(paths.personas_dir, "admin_full")
    with pytest.raises(ValueError, match="Unknown retrieval method"):
        pipeline.retrieve("test", req, method="invalid")


def test_cli_smoke(paths):
    from typer.testing import CliRunner
    from groundseal.cli.main import app

    runner = CliRunner()
    result = runner.invoke(app, ["register-source", "--manifest", str(paths.manifest)])
    assert result.exit_code == 0

    result = runner.invoke(app, ["ingest"])
    assert result.exit_code == 1  # requires --all or --source-id
