# Task Inventory

Tasks are grouped by priority and mapped to roadmap phases. Each task should leave a concrete artifact. Avoid vague tasks such as "implement RAG" or "make it enterprise-grade."

For the consolidated phase sequence, dependencies, milestones, and immediate execution order, see [docs/development-plan.md](docs/development-plan.md).

## Now

These tasks belong to Phase 0: framing and contracts.

1. Review all Phase 0 documents for consistency.
   - Phase: 0
   - Output: edits to README, project brief, roadmap, and agent rules
   - Mode: documentation first
   - Exit: no contradictions between project positioning, roadmap, and rules

2. Create a phase checklist template.
   - Phase: 0
   - Output: a reusable notes or report template
   - Mode: documentation first
   - Exit: future agents can record goal, hypothesis, artifacts, tests, findings, and next steps

3. Define source registration fields.
   - Phase: 1
   - Output: design note listing required source metadata
   - Mode: document first, experiment later, implementation later
   - Exit: source identity, ownership, permission scope, freshness, and citation fields are named

4. Draft ingestion contract examples.
   - Phase: 1
   - Output: example records in documentation, not executable code
   - Mode: document first
   - Exit: normalized document and chunk concepts are concrete enough for review

5. Define evaluation case schema.
   - Phase: 9
   - Output: evaluation-plan update with fields for query, expected evidence, permission scope, and notes
   - Mode: document first, experiment later
   - Exit: evaluation cases can be created before retrieval code exists

## Next

These tasks prepare the first implementation phases but should still begin with documents.

1. Design chunking baseline.
   - Phase: 2
   - Output: chunking strategy note under docs or notes
   - Mode: document first, experiment later, implementation later
   - Exit: chunk size, overlap, boundary rules, and traceability requirements are defined

2. Specify lexical retrieval baseline behavior.
   - Phase: 3
   - Output: retrieval-scope update and evaluation expectations
   - Mode: document first, implementation later
   - Exit: candidate fields, ranking output, and test cases are described

3. Specify semantic retrieval baseline behavior.
   - Phase: 4
   - Output: retrieval-scope update and model/provider decision note
   - Mode: document first, implementation later
   - Exit: embedding choice criteria are explicit, even if no provider is chosen yet

4. Design permission filtering test matrix.
   - Phase: 6
   - Output: permission-model update with allow, deny, partial, and missing metadata cases
   - Mode: document first, experiment later
   - Exit: permission correctness can be tested independently of generation

5. Define citation packing output contract.
   - Phase: 7
   - Output: citation-model update with packed evidence examples
   - Mode: document first, implementation later
   - Exit: citation objects support source, chunk, span, and confidence notes

6. Create failure report format.
   - Phase: 10
   - Output: template in reports or docs
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
