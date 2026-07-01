# Design Principles

## Purpose

This document defines the principles that should guide future design and implementation decisions. It exists to keep the project coherent across long-running human and AI collaboration.

## Principle 1: Retrieval Before Generation

The project should make retrieval behavior inspectable before adding a conversational layer. If retrieval cannot explain its candidates, permissions, and citations, generation will only make failures harder to see.

Tradeoff:

- Delaying generation slows visible demo progress.
- It improves understanding of the system behavior that actually determines grounded answer quality.

## Principle 2: Evidence Has Identity

Every source, document, chunk, candidate, and citation should have stable identity. Evidence without identity cannot be evaluated, debugged, cited, or permissioned reliably.

Tradeoff:

- More metadata creates design overhead.
- Less metadata makes later evaluation and auditing fragile.

## Principle 3: Permissions Are Retrieval Behavior

Permission checks should be part of candidate eligibility, not a display rule. The retrieval layer should be able to show whether a query failed because evidence was not found or because evidence was not accessible.

Tradeoff:

- Permission-aware evaluation is more complex than open retrieval.
- The added complexity is central to enterprise-oriented retrieval.

## Principle 4: Citations Are A Contract

Citations should be produced from source and chunk metadata, not guessed after an answer is generated. A citation should help inspect both relevance and permission correctness.

Tradeoff:

- Citation-first design constrains chunking and context packing.
- It prevents later systems from treating references as decorative labels.

## Principle 5: Baselines Before Complexity

The project should establish simple baselines before adding hybrid retrieval, reranking, or generation. A complex layer is only valuable if it improves known weaknesses.

Tradeoff:

- Baseline work can feel slower than adding advanced features.
- It creates the comparison needed to know whether advanced features helped.

## Principle 6: Evaluation Before Claims

The project should not claim quality based on examples alone. Claims should be backed by evaluation cases, metrics, and failure analysis.

Tradeoff:

- Evaluation requires careful case construction.
- It makes project progress credible and resume-relevant.

## Principle 7: Small Phase Exits

Each phase should end with concrete artifacts: documents, contracts, examples, tests, findings, or reports. Avoid large ambiguous milestones.

Tradeoff:

- Smaller phases require more planning discipline.
- They make long-running agent collaboration safer and easier to resume.

## Principle 8: Dependencies Must Earn Their Place

External frameworks and services should be added only when the phase needs them and the tradeoff is documented. The project should not grow by importing abstractions before it understands its own contracts.

Tradeoff:

- Conservative dependency choices can slow early implementation.
- They preserve clarity while the core retrieval behavior is still being learned.

## Principle 9: Failures Are Project Assets

Bad retrieval results, permission mistakes, missing citations, and confusing rankings should be recorded. A failure that creates a clear follow-up task is progress.

Tradeoff:

- Recording failures takes time.
- It prevents repeated mistakes and demonstrates mature engineering practice.

## Principle 10: Documentation Must Be Operational

Documentation should tell future agents what to do, what to avoid, and how to know whether work is complete. It should not be written only to look comprehensive.

Tradeoff:

- Operational documentation is more specific and needs maintenance.
- It enables consistent long-term execution.
