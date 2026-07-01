# Architecture

## Purpose

This document defines the conceptual architecture for GroundSeal RAG. It is not an implementation plan. Its job is to preserve system boundaries so future work does not collapse into a chatbot demo or an unstructured collection of retrieval scripts.

## Architectural Position

GroundSeal RAG is the retrieval and evidence assembly layer for grounded agents. It sits between enterprise knowledge sources and any downstream agent or answer generator.

The architecture should optimize for:

- source traceability
- permission correctness
- retrieval quality
- citation fidelity
- repeatable evaluation
- clear failure analysis

## Conceptual Components

1. Source registry
   - Records source identity, ownership, type, freshness, and permission metadata.
   - Prevents ingestion from becoming anonymous text loading.

2. Ingestion contract
   - Describes how raw content becomes normalized document records.
   - Preserves source identifiers and metadata required for permissions and citations.

3. Chunk inventory
   - Stores retrievable evidence units with stable identifiers.
   - Maintains boundaries, parent document identity, and citation references.

4. Lexical retriever
   - Finds candidates using exact or sparse term matching.
   - Provides a strong baseline for names, identifiers, and precise terminology.

5. Semantic retriever
   - Finds candidates by meaning similarity.
   - Helps with paraphrase and conceptual queries.

6. Hybrid merger
   - Combines lexical and semantic candidates.
   - Deduplicates evidence and exposes ranking tradeoffs.

7. Permission filter
   - Removes candidates that the requester is not allowed to access.
   - Must operate before context is passed downstream.

8. Optional reranker
   - Reorders allowed candidates for query relevance.
   - Should be justified by evaluation gains.

9. Citation packer
   - Selects evidence and citation references under a context budget.
   - Produces a traceable package for downstream use.

10. Evaluation harness
   - Measures retrieval, permission correctness, and citation behavior.
   - Produces reports and failure records.

11. Optional generation layer
   - Consumes citation-packed evidence.
   - Must not retrieve or invent context independently.

## Grounded Means

Grounded means downstream outputs are constrained by retrieved evidence whose source and permissions can be inspected. A grounded system is not only one that uses documents. It is one where the evidence path can be audited.

## Permission-Aware Means

Permission-aware means access scope affects retrieval output. The system must distinguish between evidence that is irrelevant and evidence that is relevant but inaccessible. These are different failure and evaluation categories.

## Hybrid Means

Hybrid retrieval combines lexical and semantic retrieval so that exact-match and meaning-based evidence can complement each other. Hybrid is not automatically better. It must be measured against separate baselines.

## Citation-First Means

Citation-first means every selected evidence item should retain enough source identity to be cited. Citation data should be designed before answer rendering.

## Evaluation-First Means

Evaluation-first means system changes should be connected to testable expectations. Each retrieval layer should be measured before the next layer is treated as an improvement.

## Future Tradeoffs

- Filtering before ranking may improve security simplicity but can reduce ranking context.
- Ranking before filtering may improve candidate analysis but risks mishandling restricted evidence.
- Smaller chunks can improve citation precision but harm context completeness.
- Larger chunks can preserve context but make citations less precise.
- Hybrid retrieval can increase recall but make ranking harder to explain.
- Reranking can improve quality but adds cost, latency, dependency, and evaluation burden.

## Common Failure Modes

- Anonymous chunks that cannot be traced to sources.
- Permission metadata missing or applied after context assembly.
- Hybrid retrieval increasing noisy candidates without measurable gain.
- Citations pointing to broad documents instead of specific evidence.
- Evaluation cases that only test happy paths.
- Generation layer hiding retrieval defects.

## Experiment Organization

Future experiments should isolate one variable at a time where possible. For example, compare chunk size while holding retrieval method constant, or compare lexical and semantic retrieval on the same query set. Each experiment should produce a short report with hypothesis, setup, observations, conclusion, and next steps.
