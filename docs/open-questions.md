# Open Questions

## Purpose

This document collects research and experiment questions for GroundSeal RAG. Some questions can be answered during design. Others should wait until implementation and evaluation data exist.

## Chunking Questions

- What chunk size gives the best balance between citation precision and semantic completeness?
- Should chunk boundaries follow paragraphs, headings, tokens, sentences, or source-specific structure?
- How much overlap is useful before it creates redundant retrieval results?
- How should tables, bullet lists, and policy sections be chunked?
- Should chunks carry neighboring context for citation display or retrieval only?

Questions to wait for implementation:

- Which chunk size improves recall at k on the first evaluation set?
- Does overlap improve semantic retrieval or mostly increase duplicates?

## Lexical Versus Semantic Questions

- Which query types are best served by lexical retrieval?
- Which query types are best served by semantic retrieval?
- Where does semantic retrieval miss exact identifiers that lexical retrieval finds?
- Where does lexical retrieval miss paraphrased intent that semantic retrieval finds?
- Should hybrid retrieval use fixed weights, rank fusion, or query-dependent logic?

Questions to wait for implementation:

- Does hybrid retrieval improve top-k precision or only recall?
- Which failure categories are reduced by semantic retrieval?

## Reranking Questions

- When is reranking worth the extra latency and dependency cost?
- Should reranking happen before or after permission filtering?
- Does reranking improve citation quality or only candidate ordering?
- Which failures are true ranking failures rather than missing-candidate failures?

Questions to wait for implementation:

- How much does reranking improve mean reciprocal rank on the evaluation set?
- Does reranking introduce regressions on exact-match cases?

## Permission Filtering Questions

- What is the safest default when permission metadata is missing?
- How should evaluation distinguish inaccessible relevant evidence from missing evidence?
- Should denied candidates be counted internally for diagnostics?
- How can reports avoid leaking restricted source details?
- How does permission filtering affect recall for limited-access users?

Questions to wait for implementation:

- What is the observed gap between global recall and allowed recall?
- Which permission false deny cases are caused by metadata design?

## Citation Packing Questions

- What is the minimum citation data needed for useful inspection?
- Should citation packing prefer diversity across sources or strongest individual evidence?
- How much evidence text should be included in a context package?
- How should redundant chunks from the same source be handled?
- How should citations behave when evidence is insufficient?

Questions to wait for implementation:

- Does citation packing improve downstream answer faithfulness?
- Which packing strategy best balances precision and context coverage?

## Evaluation Set Questions

- How many cases are enough for each phase?
- Should relevance be binary or graded?
- How should ambiguous queries be represented?
- How should permission context be encoded in each case?
- Should evaluation cases include expected failures?

Questions to wait for implementation:

- Which metrics are most useful for early iteration?
- Which failure categories dominate the first corpus?

## Enterprise-Oriented Questions

- Which permission model is realistic enough without becoming too complex?
- How should source freshness affect retrieval?
- Should audit logs be part of the retrieval contract?
- How should tenant boundaries be represented?
- Which extensions strengthen the project without turning it into platform sprawl?

## Questions Not To Answer Yet

- Which final app UI should the project have?
- Which production vector database should be used?
- Which LLM provider should generate answers?
- How should multi-agent workflows be orchestrated?

These questions should wait until retrieval, permissions, citations, and evaluation have stronger foundations.
