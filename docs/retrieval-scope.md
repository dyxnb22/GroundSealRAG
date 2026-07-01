# Retrieval Scope

## Purpose

This document defines what retrieval means in GroundSeal RAG and which retrieval capabilities should be explored. It prevents the project from treating retrieval as a black box behind a chat interface.

## Retrieval Objective

The retrieval layer should return a ranked, permission-valid, citation-ready set of evidence candidates for a query and requester context. The output should be inspectable before any generation step.

## In Scope

- source-aware document records
- chunk inventories with stable identifiers
- lexical retrieval baseline
- semantic retrieval baseline
- hybrid candidate merging
- metadata filtering
- permission filtering
- reranking experiments
- citation-ready evidence selection
- retrieval evaluation and failure analysis

## Out Of Scope For Early Phases

- chatbot UI
- autonomous agent workflows
- model-generated answers
- multi-step tool use
- production connectors
- distributed search infrastructure
- complex orchestration frameworks

These may become relevant later, but they should not define the early project.

## Candidate Record Expectations

Future retrieval candidates should preserve:

- query identifier or query text
- source identifier
- document identifier
- chunk identifier
- chunk boundary information
- retrieval method
- raw score or rank
- normalized score if used
- permission decision
- citation reference
- failure or warning flags if applicable

## Lexical Retrieval

Lexical retrieval should be the first retrieval baseline because it is explainable, useful for exact terms, and easy to compare. It is especially important for names, IDs, product terms, policy labels, and uncommon phrases.

Failure modes:

- misses paraphrases
- overweights repeated terms
- struggles with synonym-heavy queries
- retrieves exact matches that are contextually wrong

## Semantic Retrieval

Semantic retrieval should be introduced after lexical behavior is measured. It should help with paraphrase, conceptual similarity, and queries that do not share vocabulary with target evidence.

Failure modes:

- retrieves plausible but imprecise evidence
- weak on exact identifiers
- depends on embedding model behavior
- may blur permission-sensitive distinctions if metadata is weak

## Hybrid Retrieval

Hybrid retrieval should combine lexical and semantic candidates only after both baselines exist. The project should compare merge strategies such as rank fusion, weighted scoring, or method-specific cutoffs.

Failure modes:

- more candidates without better evidence
- duplicated chunks dominating results
- score normalization hiding retrieval method behavior
- higher recall but worse top-k precision

## Reranking

Reranking should be optional and evidence-driven. It becomes worthwhile when baseline ranking frequently retrieves the right evidence but places it too low.

Failure modes:

- increased latency and dependency cost
- overfitting to a small evaluation set
- improving relevance while hiding citation or permission errors

## Metadata And Permission Filtering

Metadata filtering narrows evidence by structured attributes. Permission filtering narrows evidence by requester access. They are related but not identical. A document can match a metadata filter and still be inaccessible.

Future experiments should measure how filters affect recall, precision, and failure categories.

## Experiment Organization

Retrieval experiments should use the same evaluation cases whenever possible. Each experiment should report:

- retrieval method
- corpus state
- query set
- permission context
- metrics
- representative successes
- representative failures
- next changes
