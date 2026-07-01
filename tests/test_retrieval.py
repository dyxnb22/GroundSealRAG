import json
import pytest

from groundseal.bootstrap import bootstrap
from groundseal.paths import ProjectPaths, find_project_root
from groundseal.permissions.requester import load_requester


@pytest.fixture
def paths():
    return ProjectPaths(find_project_root())


@pytest.fixture
def pipeline(paths):
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


def test_cli_smoke(paths, tmp_path, monkeypatch):
  pytest.importorskip("typer")
  from typer.testing import CliRunner
  from groundseal.cli.main import app

  runner = CliRunner()
  result = runner.invoke(app, ["register-source", "--manifest", str(paths.manifest)])
  assert result.exit_code == 0
