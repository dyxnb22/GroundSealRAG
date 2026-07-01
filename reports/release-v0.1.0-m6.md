# Release v0.1.0-m6

## Milestone

M6 — resume-ready permission-aware hybrid retrieval pipeline.

## Includes

- Phases 1–13 implementation
- Code review optimizations (index integrity, permissions, caching)
- 12-source corpus, 36 eval cases
- CLI: `build`, `experiment chunk-size`, ingest auto-rechunk
- CI: GitHub Actions `verify.yml`
- Chunk size experiment report

## Verify

```bash
pip install -e ".[dev]"
bash scripts/verify.sh
```

## Blocking metrics at release

- unauthorized_in_top_k: 0
- citation_leakage: 0
- eval suite: 36/36 passed
