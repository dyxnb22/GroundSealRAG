# Chunk Size Experiment Report

## Purpose
Compare retrieval metrics across chunk size strategies on the same eval suite.

## Results

| strategy | size | overlap | chunks | recall@k | MRR | passed | unauthorized |
|----------|------|---------|--------|----------|-----|--------|--------------|
| baseline-384 | 384 | 48 | 250 | 0.972 | 0.972 | 36/36 | 0 |
| baseline-512 | 512 | 64 | 204 | 0.972 | 0.972 | 36/36 | 0 |
| baseline-768 | 768 | 96 | 175 | 0.972 | 0.972 | 36/36 | 0 |

## Conclusion

Best MRR on this suite: **baseline-384** (size=384, overlap=48).

Follow-up: adopt winner as default only if permission and citation metrics remain zero.
