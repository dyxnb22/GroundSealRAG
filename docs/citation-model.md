# Citation Model

## Purpose

This document defines how GroundSeal RAG should think about citations before implementing retrieval or generation. Citations are part of the evidence contract, not a final formatting step.

## Citation Goal

A citation should let a user or evaluator inspect why a piece of evidence was used. It should connect an answer or context package back to source material with enough precision to debug relevance, freshness, and permission behavior.

## Citation-Ready Evidence

Future citation-ready evidence should include:

- source identifier
- source title or display name
- document identifier
- chunk identifier
- optional span or section reference
- retrieval method
- rank or selection order
- permission decision
- citation label
- excerpt or evidence text if allowed

## Citation Packing

Citation packing is the process of selecting evidence under a context budget while preserving traceability. It should answer:

- which evidence is included?
- which evidence was excluded?
- why was it selected?
- which source does it cite?
- is the requester allowed to see it?
- does it overlap with other evidence?

Citation packing should happen after permission filtering and before optional generation.

## Relationship To Chunking

Chunking affects citation quality directly. If chunks are too large, citations become vague. If chunks are too small, citations may lose context. The citation model should push chunking toward evidence units that are both readable and traceable.

## Relationship To Permissions

Citations must not expose inaccessible source details. A citation package should only contain source information that the requester is allowed to inspect. Permission decisions should therefore shape both evidence inclusion and citation display.

## Relationship To Evaluation

Citation evaluation should measure whether selected citations:

- point to the expected source
- identify the relevant evidence
- avoid unsupported claims
- exclude inaccessible evidence
- preserve enough context to verify downstream answers

## Common Failure Modes

- citation labels point to documents but not evidence.
- citations are generated after the answer and do not match retrieved chunks.
- retrieved evidence is correct but citation metadata is missing.
- citation packing selects redundant evidence and misses diverse support.
- citations expose restricted document titles or paths.
- answer text uses evidence that is not represented in citations.

## Future Tradeoffs

- More precise citations improve auditability but may require finer chunk boundaries.
- More citations can improve transparency but consume context budget.
- Short excerpts are easier to scan but may omit important conditions.
- Source-level citations are easy to implement but weak for failure analysis.

## Experiment Organization

Future citation experiments should compare packing strategies on the same query set. Reports should include examples where citation packing improved answer support and examples where it selected misleading, redundant, or incomplete evidence.
