# Hybrid Merge Strategy

## Default: Reciprocal Rank Fusion (RRF)

- **k**: 60
- **Formula**: `score(chunk) = sum(1 / (k + rank_i))` across retrieval methods
- **Deduplication**: by `chunk_id`; keep best contributing method scores in metadata

## Fallback

Weighted average of normalized scores with α=0.5 if RRF produces ties on all candidates.

## Evaluation

Compare hybrid vs lexical-only and semantic-only on HYB-01 through HYB-04.
