# Agent Working Guide

This file defines how AI agents and human collaborators should work in GroundSeal RAG.

## Default Posture

GroundSeal RAG is retrieval-first, permission-aware, citation-first, and evaluation-first. Agents should preserve that identity in every task. When a requested change feels like it is turning the project into a generic chatbot, return to [PROJECT_BRIEF.md](PROJECT_BRIEF.md) and realign the scope.

## Work Order

1. Identify the roadmap phase for the task.
2. Read the relevant design documents before editing.
3. Clarify the intended artifact and exit criteria.
4. Update documentation or planning before implementation.
5. Make the smallest useful change.
6. Leave notes, findings, or a report when the work produces decisions.
7. Record failures and open questions instead of hiding them.

## Phase Alignment

Every new task should state which phase it belongs to. If a task spans multiple phases, split it into smaller tasks. Do not start implementation work that cannot be mapped to [docs/roadmap.md](docs/roadmap.md).

If the roadmap is outdated, update the roadmap before making a large change.

## Current Phase Constraint

Phase 0 is documentation and contracts only. Do not add:

- retrieval implementation code
- Python package skeletons
- app, web, frontend, or API surfaces
- model API integrations
- demo scripts
- mock business logic
- broad empty directories that imply an architecture not yet earned

## Retrieval-First Rule

Do not start from generation. The system should first be able to explain:

- what sources are known
- what chunks exist
- what metadata is required
- what candidates were retrieved
- what permissions applied
- what citations were selected
- how retrieval quality was evaluated

## Permission-Aware Rule

Permission handling is not optional. Any future retrieval design must explain where permission scope is represented, when filtering occurs, how filtered candidates are counted, and how permission-related failures are evaluated.

Do not add a retrieval feature that assumes all documents are globally visible unless the phase explicitly says the experiment is permission-free and temporary.

## Citation-First Rule

Citations are part of the retrieval output contract. Future retrieval results should preserve enough source identity to support citations, audits, and failure analysis. Do not design chunks or candidate records that cannot be traced back to source documents.

## Evaluation-First Rule

Every experiment must include:

- purpose
- hypothesis
- setup
- observations
- conclusion
- follow-up work

Failed experiments are valuable project artifacts. Record them in notes or reports.

## Documentation Quality

Documentation must guide future execution. Avoid text that exists only to make the repository look complete. A good document should answer:

- what decision does this document support?
- what should a future agent do next?
- what tradeoffs matter?
- what failure modes should be watched?
- what output would prove progress?

## Implementation Gate

Before writing code in a future phase, confirm:

- the task maps to a roadmap phase
- the relevant document states the expected behavior
- the artifact has a small exit criterion
- there is a plan for at least minimal verification
- the change does not introduce unrelated infrastructure

## Reporting Rule

At the end of a meaningful work session, leave one of:

- a document update
- a task update
- a note under `notes/`
- a report under `reports/`
- a failure analysis entry

The project should accumulate conclusions, not just files.

## Drift Handling

If the project starts to drift toward a chatbot-first demo, broad framework adoption, or unmeasured feature growth, stop and update the relevant design document. Recenter on retrieval quality, permissions, citations, and evaluation.
