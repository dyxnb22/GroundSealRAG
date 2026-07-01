# Code Review Optimization Report

## Summary

Deep optimization pass addressing correctness, performance, security, CLI UX, and test coverage.

## Fixes Applied

### Data layer
- Removed document body from `documents.json`; content always read from `content_path`
- Atomic JSON writes for registry files (temp + rename)
- `list_documents()` returns `DocumentRecord` dataclasses

### Index integrity
- Vector index validates `chunk_ids.json` alignment on load
- Fingerprint files for chunks and vector index detect staleness
- Bootstrap rebuilds chunks/index when fingerprint mismatches

### Permissions
- `tenant_id` enforced on chunks and requesters
- `allowed_groups` intersection support
- Shared constants module (`permissions/constants.py`)
- Explicit `allowed_source_ids` grant path preserved for contractors

### Performance
- Embedding model singleton cache
- Cross-encoder singleton cache (lazy load on `--rerank` only)
- Pipeline `lru_cache` keyed by project root + chunks mtime
- `clear_pipeline_cache()` on ingest/chunk mutations

### Correctness
- Fixed `unauthorized_in_top_k` double-counting bug
- Removed semantic score `<= 0` filter that dropped valid results
- Reranker returns immutable `CandidateRecord` copies via `dataclasses.replace`
- Invalid retrieval `--method` raises explicit error
- Freshness filter wired into pipeline (`--exclude-stale`)

### CLI UX
- `ingest` requires `--all` or `--source-id`
- Clear error messages for unknown source/persona/method
- `evaluate` exits non-zero on unauthorized, leakage, or failed cases
- `chunk --force` for explicit rebuild
- `report --phase` prefers exact filename match

### Tests
- Added `test_permissions.py` (4 tests)
- Added `test_embeddings.py` (2 tests)
- Expanded retrieval/ingestion tests (16 total)

## Verification

- `pytest`: 16/16 passed
- `groundseal evaluate`: 32/32 passed, blocking metrics zero
