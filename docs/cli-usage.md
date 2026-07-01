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
groundseal build              # register + ingest + chunk + warm indexes
groundseal build --eval       # build then run eval suite
```

## Ingest with auto-rechunk

```bash
groundseal ingest --all              # rechunks when content hash changes (default)
groundseal ingest --all --no-rechunk # skip rechunk; manual `chunk --force` later
```

## Report

```bash
groundseal report --failures
```

## Answer (grounded)

```bash
groundseal answer -q "remote work core hours" -r contractor_limited
```
