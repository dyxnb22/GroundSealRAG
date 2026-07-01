# M6 Milestone Wrap-Up

## Status

**Closed.** Tag `v0.1.0-m6` on `main` marks the resume-ready retrieval milestone.

## Initial Document Requirements

| Source | Requirement | Met |
|--------|-------------|-----|
| PROJECT_BRIEF.md | Retrieval-first, permission-aware, citation-first, evaluation-first | Yes |
| docs/resume-scope.md | Minimum scope (lexical + citations + eval) | Exceeded |
| docs/resume-scope.md | Recommended scope (hybrid + permission + citation packing) | Yes — **M6** |
| docs/resume-scope.md | Enhanced scope (rerank, CLI, generation stub, reports) | Yes — **M7** with documented deferrals |
| docs/roadmap.md | Phases 1–13 artifacts and exit criteria | Yes |
| AGENTS.md | No chatbot-first drift; eval and failure records | Yes |

## Verification (2026-07-01)

```bash
bash scripts/verify.sh
```

- Unit tests: 13/13
- Integration tests: 4/4
- Eval suite: 36/36 passed
- `unauthorized_in_top_k`: 0
- `citation_leakage`: 0

## Documented Deferrals (Not Blockers)

| Item | Decision | Evidence |
|------|----------|----------|
| Rerank as default | Deferred | `reports/phase8-rerank-report.md` |
| Chunk size default | Keep 512 | `reports/chunk-size-experiment-report.md` — all strategies 36/36; 384 best MRR marginally |
| Generation layer | Template stub only | `reports/phase12-generation-report.md` — retrieval not bypassed |
| Full LLM / API integration | Out of scope for M6 | `docs/open-questions.md` |

## Housekeeping Completed in This Wrap-Up

- `docs/phase-checklist-template.md` — Phase 0 optional artifact
- Doc alignment: eval case count 36 across TASKS and reports
- `docs/open-questions.md` — resolved experiment answers from v0.1.0-m6
- GitHub Release `v0.1.0-m6`
- Obsolete draft PRs #1, #2 — close manually if still open (early planning superseded by main)

## Resume Narrative

Use the **Recommended** description in `docs/resume-scope.md`. Point reviewers to:

- `reports/phase5-hybrid-report.md`
- `reports/phase6-permission-report.md`
- `reports/phase9-eval-suite-report.md`
- `reports/failures/` for failure-driven iteration

## Next Work (Post-M6, Optional)

- Larger or domain-specific corpus
- Rerank re-evaluation when ranking failures appear
- Ollama or API generation only after new eval cases for answer faithfulness
- Production connectors, multi-tenant policies, distributed vector store — each needs its own phase and eval plan
