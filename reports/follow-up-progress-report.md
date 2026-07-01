# Follow-up Progress Report

## Phase

Post code-review continuation

## Changes

1. **Ingest change detection** — `ingest_file` compares `content_hash`; `IngestResult` tracks changed/new sources
2. **Auto-rechunk** — `groundseal ingest --all` rechunks by default when content changes (`--no-rechunk` to skip)
3. **Corpus fingerprint** — `data/registry/corpus_fingerprint.txt` drives bootstrap staleness detection
4. **`groundseal build`** — one-shot register + ingest + chunk + index warm-up (`--eval` optional)
5. **Test layering** — `@pytest.mark.integration` for slow tests; default `pytest` runs unit tests only
6. **`scripts/verify.sh`** — full local verification script

## Verification

- Unit tests: 13 passed
- Integration tests: 4 passed
- `groundseal build`: OK
- `groundseal evaluate`: 32/32 passed

## Next

- Merge PR #4 to main
- Optional: CI workflow running `scripts/verify.sh`
