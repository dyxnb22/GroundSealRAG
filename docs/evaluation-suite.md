# Evaluation Suite

## Case Count

- Seed: 10
- MVP: 18 (lex 4, sem 4, perm 6, cite 2, hyb 2) — expanded to full 28 in eval/cases/
- Full: 28

## Metrics

- Recall@5, MRR
- unauthorized_in_top_k (blocking = 0)
- citation_coverage, inaccessible_citation_leakage

## Run

```bash
groundseal evaluate --suite eval/cases/
```
