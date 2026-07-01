#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="${HOME}/.local/bin:${PATH}"

echo "==> Unit tests"
python3 -m pytest tests/ -q

echo "==> Integration tests"
python3 -m pytest tests/ -q -m integration

echo "==> Build pipeline"
groundseal build

echo "==> Evaluation suite"
groundseal evaluate --suite eval/cases/

echo "All verification passed."
