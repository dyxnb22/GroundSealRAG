## M6 — Resume-ready permission-aware hybrid retrieval

GroundSeal RAG v0.1.0-m6 delivers a working retrieval pipeline with permission filtering, citation packing, and a repeatable evaluation suite. This is a retrieval-first milestone, not a chatbot product.

### Highlights

- **Phases 1–13** — ingestion, chunking, BM25 + semantic + hybrid (RRF), permission filter, citation packer, eval runner, CLI
- **12-source corpus**, **36 eval cases**, 5 permission personas
- **Blocking metrics at release**: `unauthorized_in_top_k = 0`, `citation_leakage = 0`, **36/36 passed**
- **CI**: GitHub Actions runs `scripts/verify.sh` on push/PR to `main`
- **Documented experiments**: chunk size (384/512/768), rerank (deferred as default)

### Quick start

```bash
pip install -e ".[dev]"
groundseal build
groundseal evaluate --suite eval/cases/
bash scripts/verify.sh
```

### Key reports

- `reports/phase5-hybrid-report.md` — hybrid vs baselines
- `reports/phase6-permission-report.md` — permission filtering
- `reports/phase9-eval-suite-report.md` — full eval output
- `reports/chunk-size-experiment-report.md` — chunk strategy comparison
- `reports/phase8-rerank-report.md` — rerank deferral rationale

### Intentional deferrals

- Rerank: opt-in (`--rerank`), not default — no MRR gain on current suite
- Generation: template grounded answer layer; no LLM API integration
- Default chunk size: 512 (all strategies passed; see chunk experiment report)

### Resume framing

See `docs/resume-scope.md` (Recommended scope). Emphasize permission-aware hybrid retrieval, citation traceability, and evaluation-driven iteration — not a generic RAG chatbot.
