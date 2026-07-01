# GroundSeal RAG

[![Verify](https://github.com/dyxnb22/GroundSealRAG/actions/workflows/verify.yml/badge.svg)](https://github.com/dyxnb22/GroundSealRAG/actions/workflows/verify.yml)

A permission-aware hybrid retrieval system for grounded enterprise agents.

GroundSeal RAG is a long-running learning and engineering project focused on the retrieval layer behind grounded enterprise agents. The project starts from source control, document structure, permissions, citations, and evaluation before adding any generation layer. Its first milestone is not a chatbot. Its first milestone is a disciplined retrieval system that can explain what it found, why it was allowed to use it, and how well the retrieval behavior can be measured.

The repository implements Phases 1–13 of the retrieval pipeline (M6/M7 complete).

## Core Ideas

- Retrieval first: build the evidence selection layer before building a conversational interface.
- Grounded by design: every downstream answer should be traceable to retrieved evidence.
- Permission-aware: retrieval must respect access scope before context is assembled.
- Citation-first: citations are not a UI decoration; they are part of the retrieval contract.
- Evaluation-first: retrieval quality should be measured with repeatable cases, not judged by vibes.
- Small phase exits: each phase should leave concrete artifacts, findings, and next questions.

## Capability Scope

GroundSeal RAG is designed to grow toward these capabilities over time:

- source registration and ingestion planning
- document normalization and metadata contracts
- chunking strategy design
- lexical retrieval baselines
- semantic retrieval baselines
- hybrid retrieval and candidate merging
- permission scope filtering
- citation packing and evidence budgeting
- reranking experiments
- retrieval evaluation sets
- failure analysis workflows
- optional CLI surface for repeatable experiments
- optional generation layer after retrieval behavior is trustworthy

## What This Project Is

- A retrieval-first project for learning and demonstrating RAG internals.
- A grounded context assembly project where evidence quality matters more than chat polish.
- A permission-aware retrieval layer that treats access control as a core design requirement.
- A citation-first system that makes retrieved evidence inspectable.
- An evaluation-first engineering project with repeatable tests and failure records.

## What This Project Is Not

- It is not a chatbot-first demo.
- It is not a wrapper around an LLM API.
- It is not a personal notes search toy.
- It is not an enterprise product claim without measurable retrieval behavior.
- It is not a place to add frameworks, services, or abstractions before the phase requires them.

## Conceptual System Flow

The intended system can be described as a retrieval pipeline:

1. Registered sources define what documents exist, where they came from, and what metadata is required.
2. Ingestion prepares normalized document records without losing source identity.
3. Chunking creates retrievable evidence units with stable identifiers and traceable boundaries.
4. Lexical and semantic retrievers produce candidate evidence.
5. Hybrid retrieval merges, deduplicates, and ranks candidates.
6. Permission filtering removes evidence outside the requester's access scope.
7. Optional reranking improves ordering for the current query.
8. Citation packing selects evidence spans and source references for downstream use.
9. A grounded context package is passed to an optional answer layer.
10. Evaluation and failure analysis measure whether the pipeline behaves correctly.

The generation layer is deliberately optional and late. The central object of this project is the retrieval and evidence assembly contract.

## Documentation Map

- [PROJECT_BRIEF.md](PROJECT_BRIEF.md): project definition, motivation, audience, value, and non-goals.
- [AGENTS.md](AGENTS.md): working rules for future AI agents and human collaborators.
- [TASKS.md](TASKS.md): prioritized task inventory mapped to phases and artifacts.
- [docs/architecture.md](docs/architecture.md): conceptual architecture and system boundaries.
- [docs/design-principles.md](docs/design-principles.md): design principles and tradeoffs.
- [docs/retrieval-scope.md](docs/retrieval-scope.md): retrieval capabilities, boundaries, and expected experiments.
- [docs/permission-model.md](docs/permission-model.md): permission-aware retrieval concepts and risks.
- [docs/citation-model.md](docs/citation-model.md): citation contracts, packing, and evidence traceability.
- [docs/evaluation-plan.md](docs/evaluation-plan.md): retrieval evaluation strategy.
- [docs/failure-analysis-plan.md](docs/failure-analysis-plan.md): how failures should be recorded and converted into work.
- [docs/roadmap.md](docs/roadmap.md): phased execution plan from framing to enterprise-oriented extensions.
- [docs/execution-rhythm.md](docs/execution-rhythm.md): operating rhythm for long-running agent work.
- [docs/resume-scope.md](docs/resume-scope.md): how the project can become resume-ready without overstating it.
- [docs/open-questions.md](docs/open-questions.md): research and experiment questions for later phases.

## Current Status

The repository implements Phases 1–13 of the retrieval pipeline:

- Source registration, ingestion, and chunking
- Lexical (BM25), semantic, and hybrid (RRF) retrieval
- Permission-aware filtering (deny-by-default)
- Citation packing
- Evaluation suite (36 cases) and failure analysis workflow
- CLI (`groundseal`) for local experiments
- Optional grounded answer generation
- Audit log and source freshness extensions
- Corpus: 12 markdown sources in `corpus/sources/`

```bash
pip install -e ".[dev]"
groundseal build              # register + ingest + chunk + index
groundseal evaluate --suite eval/cases/
# Or step-by-step:
# groundseal register-source --manifest corpus/manifest.yaml
# groundseal ingest --all     # auto-rechunks on content change
# groundseal retrieve -q "API token rotation" -r engineer_std --method hybrid --pack
```

Full verification: `bash scripts/verify.sh`. Chunk experiment: `bash scripts/run_chunk_experiment.sh`.

## Release

- **v0.1.0-m6** — M6 resume-ready retrieval pipeline (hybrid + permission + citation + eval)

## Execution Route

The project should advance through small, reviewable phases:

1. Complete framing and contracts.
2. Define source and document records before ingestion code.
3. Design chunking and metadata contracts before retrieval code.
4. Add lexical retrieval before semantic retrieval.
5. Measure lexical and semantic baselines before hybrid retrieval.
6. Add permission filtering before answer generation.
7. Add citation packing before a generation layer.
8. Build evaluation and failure analysis as first-class project outputs.

Long-term evolution should preserve the same rule: every new layer must improve traceability, permission correctness, retrieval quality, or evaluation clarity.
