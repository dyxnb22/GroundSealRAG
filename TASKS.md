# Task Inventory

Tasks mapped to roadmap phases 0–13. Each task leaves a concrete artifact.

## Phase 0 — Complete

## Phase 1–13 — Complete

- [x] Source registry and markdown ingestion
- [x] Chunking baseline
- [x] Lexical, semantic, hybrid retrieval
- [x] Permission filtering
- [x] Citation packing
- [x] Evaluation suite (36 cases)
- [x] Failure analysis workflow
- [x] CLI surface
- [x] Reranking (opt-in, defer as default)
- [x] Grounded generation
- [x] Audit log + freshness extensions

## Follow-up (post-review)

- [x] Ingest content-hash change detection with auto-rechunk
- [x] Corpus fingerprint for index staleness
- [x] `groundseal build` one-shot setup command
- [x] `scripts/verify.sh` full verification script
- [x] pytest integration marker (fast default, `-m integration` for slow)

## Release & CI (complete)

- [x] Merge to `main` and tag `v0.1.0-m6`
- [x] GitHub Actions CI (`.github/workflows/verify.yml`)
- [x] Corpus extended to 12 sources + 4 eval cases (`eval/cases/ext.yaml`)
- [x] Chunk size experiment (384/512/768) — `reports/chunk-size-experiment-report.md`

## M6 Wrap-Up (complete)

- [x] Milestone closure report — `reports/m6-milestone-wrap-up.md`
- [x] Phase checklist template — `docs/phase-checklist-template.md`
- [x] Doc alignment (36 eval cases, open-questions resolutions)
- [x] GitHub Release `v0.1.0-m6`
- [x] Close obsolete draft PRs (#1, #2)
