# CLI Usage

## Setup

```bash
pip install -e ".[dev]"
groundseal register-source --manifest corpus/manifest.yaml
groundseal ingest --all
groundseal chunk --strategy baseline
```

## Retrieve

```bash
groundseal retrieve -q "API token rotation" -r engineer_std --method hybrid --pack
```

## Evaluate

```bash
groundseal evaluate --suite eval/cases/ --report reports/phase9-eval-suite-report.md
```

Exits non-zero on: `unauthorized_in_top_k > 0`, citation leakage, or any failed case.

## Rebuild index

```bash
groundseal chunk --force
```

## Report

```bash
groundseal report --failures
```

## Answer (grounded)

```bash
groundseal answer -q "remote work core hours" -r contractor_limited
```
