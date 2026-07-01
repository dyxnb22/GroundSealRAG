#!/usr/bin/env bash
# Compare chunk strategies locally (not part of CI — slower).
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="${HOME}/.local/bin:${PATH}"

groundseal ingest --all
groundseal experiment chunk-size --report reports/chunk-size-experiment-report.md
groundseal build
groundseal evaluate --suite eval/cases/
echo "Chunk experiment complete."
