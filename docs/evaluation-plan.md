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

The core evaluation unit should be a query case. A query case should eventually include:

- case identifier
- query text
- requester or permission context
- expected relevant source or chunk identifiers
- expected inaccessible evidence if relevant
- acceptable alternate evidence
- required citation behavior
- notes about ambiguity
- failure category if known

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
