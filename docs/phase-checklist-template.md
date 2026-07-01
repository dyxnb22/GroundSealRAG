# Phase Checklist Template

## Purpose

Use this template at the end of each roadmap phase. Copy the section for the active phase, fill it in, and save the result under `reports/` or `notes/`.

## Phase N — [Name]

### Alignment

- Roadmap phase: [N]
- Related design docs: [list]
- Intended artifact: [one sentence]

### Required Artifacts

- [ ] [artifact 1]
- [ ] [artifact 2]

### Exit Criteria

- [ ] [criterion from roadmap]
- [ ] [criterion from roadmap]

### Evaluation

- Cases run: [command or suite path]
- Blocking metrics: [e.g. unauthorized_in_top_k = 0]
- Non-blocking metrics: [recall@k, MRR, etc.]

### Observations

- What worked:
- What failed:
- Surprises:

### Failure Modes Watched

- [ ] [failure category]
- [ ] [failure category]

### Conclusion

[Accept / defer / reject — one paragraph with evidence]

### Follow-up Tasks

- [ ] [specific next task mapped to a phase]
- [ ] [doc or eval update if needed]

## Quick Reference — Phase Exit Artifacts

| Phase | Primary artifact |
|-------|------------------|
| 0 | Consistent contracts, no implementation code |
| 1 | Source/document contracts, ingestion boundaries |
| 2 | Chunk record contract, baseline strategy |
| 3 | Lexical baseline + failure examples |
| 4 | Semantic baseline + lexical comparison |
| 5 | Hybrid merge strategy + comparison report |
| 6 | Permission filter + test matrix |
| 7 | Citation packer + packing examples |
| 8 | Rerank experiment with accept/defer/reject |
| 9 | Eval suite + reproducible report |
| 10 | Failure taxonomy + categorized records |
| 11 | CLI commands with traceable I/O |
| 12 | Grounded generation consuming citations only |
| 13 | Extension proposal with evaluation evidence |
