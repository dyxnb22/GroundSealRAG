# Task Inventory

Tasks are grouped by priority and mapped to roadmap phases. Each task should leave a concrete artifact. Avoid vague tasks such as "implement RAG" or "make it enterprise-grade."

For the consolidated phase sequence, dependencies, milestones, and immediate execution order, see [docs/development-plan.md](docs/development-plan.md).

## Now

These tasks belong to Phase 1 and Phase 2 preparation.

1. Review Phase 1 contracts for approval.
   - Phase: 1
   - Output: approved `docs/source-registration-contract.md`, `docs/ingestion-contract.md`, `docs/first-corpus-plan.md`
   - Mode: documentation review
   - Exit: contracts ready for optional minimal source registry implementation

2. Design chunking baseline.
   - Phase: 2
   - Output: chunking strategy note under `docs/` or `notes/`
   - Mode: document first, experiment later, implementation later
   - Exit: chunk size, overlap, boundary rules, and traceability requirements are defined

3. Create corpus markdown files for first corpus.
   - Phase: 1–2 prep
   - Output: markdown files matching `docs/first-corpus-plan.md` inventory
   - Mode: documentation / corpus prep
   - Exit: files exist for ingestion or chunking experiments

4. Assign chunk IDs in seed evaluation cases.
   - Phase: 2
   - Output: updated `notes/seed-evaluation-cases.md` with chunk references
   - Mode: document first
   - Exit: cases reference stable chunk identifiers

## Next

These tasks prepare the first implementation phases but should still begin with documents.

1. Specify lexical retrieval baseline behavior.
   - Phase: 3
   - Output: retrieval-scope update and evaluation expectations
   - Mode: document first, implementation later
   - Exit: candidate fields, ranking output, and test cases are described

2. Specify semantic retrieval baseline behavior.
   - Phase: 4
   - Output: retrieval-scope update and model/provider decision note
   - Mode: document first, implementation later
   - Exit: embedding choice criteria are explicit, even if no provider is chosen yet

3. Design permission filtering test matrix.
   - Phase: 6
   - Output: permission-model update with allow, deny, partial, and missing metadata cases
   - Mode: document first, experiment later
   - Exit: permission correctness can be tested independently of generation

4. Define citation packing output contract.
   - Phase: 7
   - Output: citation-model update with packed evidence examples
   - Mode: document first, implementation later
   - Exit: citation objects support source, chunk, span, and confidence notes

5. Create failure report format.
   - Phase: 10
   - Output: template in `reports/` or `docs/`
   - Mode: documentation first
   - Exit: each retrieval failure can be classified and turned into follow-up work

## Later

These tasks should wait until the earlier phases produce artifacts and findings.

1. Implement minimal source registry.
   - Phase: 1
   - Output: small implementation only after source contract is approved
   - Mode: implementation after documentation
   - Exit: can list registered sources with required metadata

2. Implement chunking baseline.
   - Phase: 2
   - Output: small chunking module or script
   - Mode: implementation after document and examples
   - Exit: chunks have stable identifiers and source references

3. Implement lexical retrieval baseline.
   - Phase: 3
   - Output: repeatable retrieval command or test harness
   - Mode: implementation after evaluation cases exist
   - Exit: baseline metrics and failure notes are recorded

4. Implement semantic retrieval baseline.
   - Phase: 4
   - Output: embedding-based retrieval baseline
   - Mode: implementation after dependency and provider decision
   - Exit: comparison against lexical baseline is reported

5. Implement hybrid merge.
   - Phase: 5
   - Output: documented merge strategy and experiment report
   - Mode: implementation after separate baselines
   - Exit: hybrid behavior improves or clearly explains tradeoffs

6. Implement permission-aware filtering.
   - Phase: 6
   - Output: filter behavior plus permission evaluation cases
   - Mode: implementation after permission matrix
   - Exit: unauthorized evidence is excluded and reported correctly

7. Implement citation packing.
   - Phase: 7
   - Output: citation package format and examples
   - Mode: implementation after citation contract
   - Exit: every selected evidence item remains traceable

8. Add optional generation layer.
   - Phase: 12
   - Output: small answer layer that consumes retrieval packages
   - Mode: implementation only after retrieval and citation evaluation
   - Exit: generated answers never bypass retrieval evidence

## Completed

| Task | Phase | Artifact |
|------|-------|----------|
| Review Phase 0 documents for consistency | 0 | `notes/phase0-consistency-review.md` |
| Create phase checklist template | 0 | `notes/phase-checklist-template.md` |
| Phase 0 completion report | 0 | `reports/phase0-completion-report.md` |
| Consolidated development plan | 0 | `docs/development-plan.md` |
| Define source registration fields | 1 | `docs/source-registration-contract.md` |
| Draft ingestion contract examples | 1 | `docs/ingestion-contract.md` |
| Define first corpus source types | 1 | `docs/first-corpus-plan.md` |
| Define evaluation case schema | 9 prep | `docs/evaluation-plan.md`, `notes/seed-evaluation-cases.md` |
