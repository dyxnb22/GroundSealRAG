# Phase 11 CLI Report

## Commands

- register-source, ingest, chunk, retrieve, evaluate, report, answer

## Demo Path

```bash
groundseal register-source --manifest corpus/manifest.yaml
groundseal ingest --all
groundseal chunk --strategy baseline
groundseal retrieve -q "API token rotation" -r engineer_std --method hybrid --pack
groundseal evaluate --suite eval/cases/
groundseal report --failures
```

## Conclusion

CLI supports repeatable local experiments without UI/API surface.
