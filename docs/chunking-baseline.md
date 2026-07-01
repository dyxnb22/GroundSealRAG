# Chunking Baseline

## Strategies

| Strategy | Chunk size | Overlap |
|----------|------------|---------|
| `baseline` / `baseline-512` | 512 | 64 |
| `baseline-384` | 384 | 48 |
| `baseline-768` | 768 | 96 |

## Default

`baseline` (512 chars, 64 overlap), heading-aware splits.

## Experiment

```bash
bash scripts/run_chunk_experiment.sh
```

Report: `reports/chunk-size-experiment-report.md`
