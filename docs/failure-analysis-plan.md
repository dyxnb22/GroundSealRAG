# Failure Analysis Plan

## Purpose

This document defines how GroundSeal RAG should analyze and record failures. A retrieval project improves when failures are made specific enough to act on.

## Failure Analysis Goal

The goal is not to avoid failure records. The goal is to convert confusing behavior into a known category, likely cause, and next experiment.

## Failure Categories

Use these initial categories:

- source gap: the needed source was never registered or ingested.
- metadata gap: source or chunk metadata is missing or wrong.
- chunking failure: evidence exists but chunk boundaries make it hard to retrieve or cite.
- lexical miss: exact or sparse retrieval misses relevant evidence.
- semantic miss: semantic retrieval misses conceptually relevant evidence.
- ranking failure: relevant evidence is retrieved but ranked too low.
- hybrid merge failure: candidate merging suppresses or duplicates useful evidence.
- permission false allow: inaccessible evidence is returned.
- permission false deny: accessible evidence is incorrectly removed.
- citation failure: evidence is retrieved but citation output is missing, vague, or wrong.
- evaluation gap: the case cannot be judged because expected behavior is unclear.

## Failure Record Fields

A future failure record should include:

- failure identifier
- date
- phase
- query
- requester context
- expected behavior
- observed behavior
- affected sources or chunks
- failure category
- likely cause
- severity
- proposed follow-up
- conclusion after follow-up

## Relationship To Evaluation

Evaluation finds failures; failure analysis explains them. Metrics should point to cases, and cases should produce records when behavior is surprising or important.

## Relationship To Roadmap

Repeated failures should influence the roadmap. For example:

- many chunking failures should pause retrieval expansion and revisit chunk strategy.
- many permission false allows should block citation or generation work.
- many ranking failures may justify reranking.
- many citation failures should block optional generation.

## Common Failure Analysis Mistakes

- recording only the metric and not the example.
- treating permission failures as normal retrieval misses.
- changing several variables before identifying the cause.
- deleting failure notes after a fix.
- writing reports that do not produce follow-up tasks.

## Future Experiment Workflow

1. Run evaluation.
2. Identify representative failures.
3. Categorize failures.
4. Write a short failure record.
5. Propose one targeted change.
6. Re-run the affected cases.
7. Record whether the change helped, hurt, or was inconclusive.

The project should value clear negative findings. "This did not improve retrieval under these cases" is a useful conclusion.
