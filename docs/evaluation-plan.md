# Evaluation Plan

## Purpose

This document defines how GroundSeal RAG should evaluate retrieval behavior. Evaluation should begin before the project has a generation layer.

## Evaluation Goals

The evaluation system should help answer:

- Did retrieval find relevant evidence?
- Did it rank useful evidence high enough?
- Did permission filtering remove unauthorized evidence?
- Did citation packing preserve support for downstream answers?
- Did a change improve the system or only add complexity?

## Evaluation Units

The core evaluation unit is a **query case**. Cases should be authored before retrieval implementation where possible. Seed cases live in [notes/seed-evaluation-cases.md](../notes/seed-evaluation-cases.md).

### Query Case Schema

| Field | Required | Description |
|-------|----------|-------------|
| `case_id` | yes | Stable identifier, e.g. `case-001`. |
| `query_text` | yes | Natural language query. |
| `requester.persona_id` | yes | Reference persona from corpus plan. |
| `requester.tenant_id` | yes | Tenant scope for permission checks. |
| `requester.roles` | yes | Role list (may be empty). |
| `requester.groups` | yes | Group list (may be empty). |
| `expected_relevant.documents` | yes | Document IDs that should be retrieved for this requester. |
| `expected_relevant.chunks` | no | Chunk IDs; required once chunking exists. |
| `expected_inaccessible.documents` | no | Relevant globally but must not appear for this requester. |
| `expected_inaccessible.chunks` | no | Same at chunk level. |
| `acceptable_alternates` | no | Document or chunk IDs that satisfy the case if primary evidence ranks lower. |
| `required_citation_behavior` | yes | Human-readable citation expectation. |
| `permission_expectation` | yes | One of: `allow`, `deny`, `partial`. |
| `primary_metric` | yes | Main metric for this case, e.g. `recall@3`, `unauthorized_evidence_in_top_k`. |
| `notes` | no | Ambiguity, setup, or grading guidance. |
| `failure_category_if_known` | no | From failure taxonomy if this case targets a known failure mode. |

### Case Categories (First Corpus)

- `lexical_exact` — exact terms, IDs, numbers
- `semantic_paraphrase` — wording differs from source text
- `permission_allow` — allowed evidence should appear
- `permission_deny` — relevant but restricted evidence must not appear
- `permission_partial` — mixed allowed and denied sources
- `permission_no_access` — requester lacks all access
- `cross_source` — evidence from multiple allowed sources
- `no_result` — evidence absent from corpus
- `ranking_setup` — multiple candidates; order matters

### Grading Rules

1. **Permission deny cases** — any unauthorized document or chunk in top-k is a blocking failure.
2. **No-result cases** — retrieving plausible but wrong evidence is a retrieval failure, not a permission failure.
3. **Ambiguous cases** — use `acceptable_alternates` rather than leaving expected evidence vague.
4. **Global vs allowed recall** — record both when `expected_inaccessible` is non-empty.

## Metrics To Consider

Retrieval metrics:

- recall at k
- precision at k
- mean reciprocal rank
- normalized discounted cumulative gain if graded relevance is useful
- duplicate rate
- no-result rate

Permission metrics:

- unauthorized evidence in top-k
- allowed recall at k
- denied relevant evidence count
- missing-metadata cases
- permission explanation correctness

Citation metrics:

- citation coverage
- citation precision
- unsupported evidence rate
- redundant citation rate
- inaccessible citation leakage

## Baseline Strategy

Evaluation should start with small, interpretable datasets. The first goal is not statistical significance. The first goal is repeatability and useful failure signals.

Recommended order:

1. Manual gold cases for a small corpus.
2. Lexical baseline evaluation.
3. Semantic baseline evaluation on the same cases.
4. Hybrid comparison.
5. Permission-aware cases.
6. Citation packing cases.
7. Reranking ablations.

## Evaluation-First In Practice

Before implementing a retrieval method, define how it will be judged. A feature without an evaluation path should remain a design note.

Each phase should answer:

- what behavior should improve?
- what metric or observation will show that?
- what could get worse?
- what cases are most likely to reveal failures?

## Common Failure Modes

- evaluation cases only cover obvious keyword matches.
- expected evidence is too vague to judge.
- permission context is missing from cases.
- success examples are recorded but failures are not.
- metrics improve while citations get worse.
- hybrid retrieval is adopted without baseline comparison.

## Experiment Reports

Each evaluation run should leave a short report under `reports/` when implementation begins. The report should include:

- phase
- corpus version
- retrieval configuration
- query cases
- metrics
- notable successes
- notable failures
- conclusion
- follow-up tasks
