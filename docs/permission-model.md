# Permission Model

## Purpose

This document defines the permission-aware retrieval concepts for GroundSeal RAG. The goal is not to implement enterprise access control in Phase 0. The goal is to make permission scope a first-class retrieval concern.

## Permission-Aware Retrieval

Permission-aware retrieval means the system returns only evidence that the requester is allowed to access. It also means the system can distinguish among:

- evidence does not exist
- evidence exists but is not relevant
- evidence exists and is relevant but inaccessible
- evidence exists, is relevant, and is accessible

These distinctions matter for evaluation and debugging.

## Expected Permission Inputs

Future designs should consider:

- requester identifier or role
- tenant or organization scope
- team or department scope
- document owner
- document visibility level
- source-specific access labels
- sensitivity labels
- time-based access if relevant

The early project should keep this model small and inspectable.

## Permission Metadata On Evidence

Source, document, and chunk records should preserve enough metadata to decide access. Permission metadata should not be stripped during ingestion or chunking.

Field names are defined in [source-registration-contract.md](source-registration-contract.md) and copied into document records per [ingestion-contract.md](ingestion-contract.md):

| Field | Level | Purpose |
|-------|-------|---------|
| `tenant_id` | source, document, chunk | Tenant boundary |
| `source_id` | source, document, chunk | Source identity |
| `owner_id` | source, document | Ownership |
| `allowed_roles` | source, document | Role-based allow list |
| `allowed_groups` | source, document | Group-based allow list |
| `visibility` | source, document | Coarse access label |
| `sensitivity` | source, document | Sensitivity reporting |
| `policy_tags` | source (optional) | Future policy filters |

Document-level permissions may narrow source permissions but must not widen them.

## Filtering Point

The safest conceptual default is:

1. retrieve candidates
2. apply metadata filters if requested
3. apply permission filtering
4. rerank allowed candidates if the phase includes reranking
5. pack citations from allowed evidence

Future experiments may compare alternate ordering, but any design must prevent unauthorized evidence from entering the final context package.

## Permission And Recall

Permission filtering can reduce visible recall. This is not automatically a retrieval failure. Evaluation should separate global recall from allowed recall. A query may have relevant evidence in the corpus but no relevant evidence for a specific requester.

## Common Failure Modes

- missing permission metadata causes accidental allow behavior.
- filtering happens after context assembly.
- evaluation only tests users with full access.
- citation metadata exposes restricted source details.
- semantic retrieval retrieves restricted evidence that is later mishandled.
- permission filtering removes all candidates and the system reports this as "no relevant documents" without explanation.

## Future Tradeoffs

- Strict deny-by-default behavior improves safety but requires complete metadata.
- Allow-by-default behavior makes early experiments easier but is unsuitable for the project identity.
- Fine-grained permissions improve realism but can slow early learning.
- Coarse permissions are easier to test but may hide important enterprise behavior.

## Experiment Organization

Permission experiments should include at least:

- full-access requester
- limited-access requester
- no-access requester
- mixed-access query with relevant allowed and denied evidence
- missing-metadata case

Each experiment should record allowed recall, denied evidence count, citation behavior, and failure classification.
