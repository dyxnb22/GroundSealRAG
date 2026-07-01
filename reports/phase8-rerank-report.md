# Phase 8 Rerank Report

## Hypothesis

Cross-encoder reranking improves MRR on ranking failure cases.

## Setup

- Model: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- Cases: RANK-01 to RANK-03

## Observations

- Baseline hybrid MRR already 1.0 on ranking cases
- Rerank does not improve top-3 ordering on RANK-01

## Conclusion

**Defer** as default path; keep `--rerank` opt-in for future corpora where ranking failures appear.
