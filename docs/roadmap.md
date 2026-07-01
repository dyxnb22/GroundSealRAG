# Roadmap

## Purpose

This roadmap is a long-running execution map, not a one-time delivery plan. Each phase should leave concrete artifacts and should be small enough for an agent or human collaborator to complete, review, and resume.

## Phase 0: Framing And Contracts

Goal: Define the project identity, boundaries, documents, agent rules, and execution rhythm.

Why it matters: Without strong framing, the project will drift into a generic RAG chatbot or an unmeasured code pile.

Required artifacts:

- README
- project brief
- agent guide
- task inventory
- design and evaluation documents
- Cursor rules

Recommended document outputs:

- consistency review notes
- phase checklist template (`docs/phase-checklist-template.md`)

Optional implementation outputs:

- none

Evaluation criteria:

- documents agree on retrieval-first, permission-aware, citation-first, evaluation-first scope
- no business implementation code exists
- future agents can identify the next phase

Exit criteria:

- Phase 0 documents exist and are internally consistent
- tasks are mapped to phases
- code is still absent

Common risks:

- writing broad aspirational content
- adding code too early
- overclaiming enterprise maturity

Follow-up questions:

- What source examples should Phase 1 use?
- What minimum metadata fields are required?

## Phase 1: Source Registration And Ingestion Plan

Goal: Define how sources are registered and how raw content becomes normalized document records.

Why it matters: Retrieval quality and citations depend on source identity.

Required artifacts:

- source metadata contract
- document record contract
- ingestion assumptions

Recommended document outputs:

- source registration design note
- sample non-executable records

Optional implementation outputs:

- minimal source registry after contract review

Evaluation criteria:

- every document can be traced to a source
- permission and citation metadata are preserved

Exit criteria:

- source and document fields are defined
- ingestion boundaries are clear

Common risks:

- anonymous text ingestion
- missing ownership or permission metadata

Follow-up questions:

- Which source types are in the first corpus?
- How should freshness be represented?

## Phase 2: Chunking Baseline

Goal: Define and test a simple chunking strategy with stable chunk identity.

Why it matters: Chunk boundaries shape retrieval, citations, and evaluation.

Required artifacts:

- chunk record contract
- baseline chunking strategy
- chunk boundary rationale

Recommended document outputs:

- chunking design note
- examples of good and bad chunk boundaries

Optional implementation outputs:

- minimal chunking implementation

Evaluation criteria:

- chunks preserve source and document identity
- chunks are citation-ready
- chunk boundaries are inspectable

Exit criteria:

- one baseline strategy is selected
- known chunking tradeoffs are recorded

Common risks:

- chunks too large for precise citations
- chunks too small for meaning

Follow-up questions:

- What chunk sizes should be compared later?
- How should tables or lists be handled?

## Phase 3: Lexical Retrieval Baseline

Goal: Build or specify the first exact/sparse retrieval baseline.

Why it matters: Lexical retrieval is explainable and strong for precise terms.

Required artifacts:

- lexical retrieval contract
- candidate output format
- initial query cases

Recommended document outputs:

- lexical baseline report
- failure examples

Optional implementation outputs:

- minimal lexical retriever

Evaluation criteria:

- exact-term queries retrieve expected evidence
- candidate records are traceable

Exit criteria:

- lexical baseline metrics or expected metrics are recorded
- failure categories are identified

Common risks:

- treating lexical misses as general retrieval failure
- skipping candidate traceability

Follow-up questions:

- Which queries require exact-match behavior?
- What score fields should be retained?

## Phase 4: Semantic Retrieval Baseline

Goal: Add or design a semantic retrieval baseline for paraphrase and conceptual matching.

Why it matters: Semantic retrieval complements lexical retrieval when wording differs.

Required artifacts:

- embedding decision note
- semantic candidate contract
- comparison query set

Recommended document outputs:

- semantic baseline report
- lexical versus semantic comparison

Optional implementation outputs:

- minimal semantic retriever

Evaluation criteria:

- paraphrase cases improve over lexical where expected
- exact-identifier regressions are visible

Exit criteria:

- semantic strengths and weaknesses are documented
- dependency choices are justified

Common risks:

- adding embeddings before evaluation cases
- trusting semantic similarity without evidence

Follow-up questions:

- Which embedding model or local option fits the project?
- How should semantic scores be normalized?

## Phase 5: Hybrid Retrieval

Goal: Combine lexical and semantic retrieval into a measured hybrid approach.

Why it matters: Hybrid retrieval can improve recall, but only if merging is disciplined.

Required artifacts:

- merge strategy
- deduplication rule
- comparison against baselines

Recommended document outputs:

- hybrid retrieval experiment report
- rank fusion rationale

Optional implementation outputs:

- hybrid candidate merger

Evaluation criteria:

- hybrid improves selected cases or explains tradeoffs
- duplicate and noise rates are tracked

Exit criteria:

- selected merge strategy is documented
- baseline comparison is complete

Common risks:

- more candidates but worse top-k quality
- opaque score normalization

Follow-up questions:

- Should merge weights be static or query-dependent?
- How should ties be handled?

## Phase 6: Permission-Aware Filtering

Goal: Add permission scope filtering to candidate selection.

Why it matters: Enterprise retrieval must not expose unauthorized evidence.

Required artifacts:

- permission metadata contract
- requester context model
- permission test matrix

Recommended document outputs:

- permission filtering report
- false allow and false deny cases

Optional implementation outputs:

- permission filter

Evaluation criteria:

- unauthorized evidence is excluded
- allowed recall is measured separately from global recall

Exit criteria:

- permission behavior is testable
- citation packing can trust filtered candidates

Common risks:

- filtering after context assembly
- missing metadata leading to unsafe defaults

Follow-up questions:

- What should happen when metadata is missing?
- How should denied evidence be counted in reports?

## Phase 7: Citation Packing

Goal: Select citation-ready evidence under a context budget.

Why it matters: Citations make grounded retrieval inspectable.

Required artifacts:

- citation output contract
- packing strategy
- evidence budget rules

Recommended document outputs:

- citation packing examples
- citation failure notes

Optional implementation outputs:

- citation packer

Evaluation criteria:

- selected evidence remains source-traceable
- citations support expected answers
- inaccessible citations are not exposed

Exit criteria:

- citation package is stable enough for downstream use
- citation failures are categorized

Common risks:

- vague document-level citations
- redundant citations consuming context

Follow-up questions:

- How many citations should be packed by default?
- Should evidence snippets be included or referenced only?

## Phase 8: Reranking

Goal: Test whether reranking improves allowed candidate ordering.

Why it matters: Reranking may improve top-k quality after retrieval and filtering.

Required artifacts:

- reranking hypothesis
- comparison setup
- cost and dependency note

Recommended document outputs:

- reranking experiment report
- cases where reranking helps or hurts

Optional implementation outputs:

- reranker integration or local reranking baseline

Evaluation criteria:

- ranking metrics improve on meaningful cases
- permission and citation behavior do not regress

Exit criteria:

- reranking is accepted, rejected, or deferred with evidence

Common risks:

- adding cost without measurable gain
- overfitting small query sets

Follow-up questions:

- Is reranking needed before optional generation?
- Which failures are ranking failures rather than retrieval failures?

## Phase 9: Retrieval Evaluation Suite

Goal: Build a repeatable evaluation suite for retrieval, permissions, and citations.

Why it matters: Long-term progress requires repeatable measurement.

Required artifacts:

- query case schema
- gold evidence set
- metric definitions
- report format

Recommended document outputs:

- evaluation suite design
- baseline evaluation report

Optional implementation outputs:

- evaluation runner

Evaluation criteria:

- cases cover lexical, semantic, hybrid, permission, and citation behavior
- reports are reproducible

Exit criteria:

- evaluation can be run after retrieval changes
- results create actionable follow-ups

Common risks:

- small happy-path-only test set
- unclear expected evidence

Follow-up questions:

- How many cases are enough for each phase?
- How should ambiguous relevance be graded?

## Phase 10: Failure Analysis Workflow

Goal: Turn retrieval failures into categorized, actionable findings.

Why it matters: Failure analysis is how the project learns from bad results.

Required artifacts:

- failure taxonomy
- failure record template
- reporting workflow

Recommended document outputs:

- failure analysis report
- task updates from failures

Optional implementation outputs:

- failure record helper if needed

Evaluation criteria:

- failures are categorized consistently
- follow-up tasks are specific

Exit criteria:

- evaluation failures produce documented action items

Common risks:

- hiding failures behind aggregate metrics
- changing too many variables at once

Follow-up questions:

- Which failure categories are most common?
- Which failures should block generation?

## Phase 11: CLI Surface

Goal: Add a small command-line surface for repeatable local experiments.

Why it matters: A CLI can make retrieval, evaluation, and reporting easier to run without building an app.

Required artifacts:

- CLI command scope
- input and output contracts
- examples

Recommended document outputs:

- CLI usage note
- command design rationale

Optional implementation outputs:

- minimal CLI commands for indexing, retrieval, evaluation, and reporting

Evaluation criteria:

- commands support repeatable experiments
- outputs preserve traceability

Exit criteria:

- CLI improves workflow without becoming a product UI

Common risks:

- CLI scope expanding into app features
- commands hiding important intermediate data

Follow-up questions:

- Which commands are necessary for evaluation?
- What output format is best for reports?

## Phase 12: Optional Generation Layer

Goal: Add a small generation layer that consumes citation-packed evidence.

Why it matters: Generation can demonstrate grounded answers after retrieval is mature.

Required artifacts:

- generation constraints
- evidence consumption contract
- unsupported-claim checks

Recommended document outputs:

- grounded answer design note
- answer evaluation report

Optional implementation outputs:

- minimal answer generator

Evaluation criteria:

- answers cite packed evidence
- unsupported claims are detectable
- generation does not bypass retrieval

Exit criteria:

- generation adds value without hiding retrieval behavior

Common risks:

- project becoming chatbot-first
- prompts compensating for weak retrieval

Follow-up questions:

- Which provider or local model is appropriate?
- What should the generator do when evidence is insufficient?

## Phase 13: Enterprise-Oriented Extensions

Goal: Explore extensions that make the retrieval layer closer to enterprise needs.

Why it matters: Long-term value comes from realistic constraints.

Required artifacts:

- extension proposal
- risk analysis
- evaluation plan

Recommended document outputs:

- extension design notes
- comparison reports

Optional implementation outputs:

- selected extensions only

Evaluation criteria:

- extension improves traceability, permission correctness, retrieval quality, or evaluation clarity
- added complexity is justified

Exit criteria:

- extension is accepted, rejected, or deferred with documented evidence

Common risks:

- adding features because they sound enterprise-like
- broad connectors without evaluation value

Follow-up questions:

- Which extension best supports the resume narrative?
- Which extension exposes the most useful learning tradeoff?
