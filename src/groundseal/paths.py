from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectPaths:
    root: Path

    @property
    def corpus(self) -> Path:
        return self.root / "corpus"

    @property
    def manifest(self) -> Path:
        return self.corpus / "manifest.yaml"

    @property
    def sources_dir(self) -> Path:
        return self.corpus / "sources"

    @property
    def registry_dir(self) -> Path:
        return self.root / "data" / "registry"

    @property
    def chunks_path(self) -> Path:
        return self.root / "data" / "chunks" / "chunks.jsonl"

    @property
    def bm25_dir(self) -> Path:
        return self.root / "data" / "index" / "bm25"

    @property
    def vectors_dir(self) -> Path:
        return self.root / "data" / "index" / "vectors"

    @property
    def personas_dir(self) -> Path:
        return self.root / "eval" / "personas"

    @property
    def cases_dir(self) -> Path:
        return self.root / "eval" / "cases"

    @property
    def reports_dir(self) -> Path:
        return self.root / "reports"

    @property
    def failures_dir(self) -> Path:
        return self.reports_dir / "failures"

    @property
    def audit_log(self) -> Path:
        return self.root / "data" / "audit" / "retrieval.jsonl"


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for path in [current, *current.parents]:
        if (path / "pyproject.toml").exists() and (path / "corpus" / "manifest.yaml").exists():
            return path
    raise FileNotFoundError("Could not find project root with pyproject.toml and corpus/manifest.yaml")
