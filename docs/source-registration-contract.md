# Source Registration Contract

**Phase:** 1  
**Status:** Draft for review  
**Purpose:** Define required metadata for registered sources so documents, permissions, and citations remain traceable through ingestion and retrieval.

## Scope

This contract covers **source records** only. Document and chunk contracts are defined in [ingestion-contract.md](ingestion-contract.md). Permission evaluation behavior is defined in [permission-model.md](permission-model.md).

## Design Rules

1. Every ingested document must reference a registered `source_id`.
2. Permission metadata on the source must survive ingestion without being stripped.
3. Citation display fields must be present at registration time or derivable without guessing.
4. Missing required fields block registration rather than defaulting to anonymous or allow-all behavior.

## Source Record Schema

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `source_id` | string | Stable unique identifier. Format: lowercase slug with optional namespace prefix, e.g. `corp:policy-handbook`. |
| `source_type` | enum | One of: `policy_doc`, `internal_wiki`, `ticket_export`, `runbook`, `faq`, `other`. Drives ingestion assumptions. |
| `title` | string | Human-readable source name for citations and audit. |
| `owner_id` | string | Primary owner or owning team identifier. |
| `tenant_id` | string | Organization or tenant boundary. Required even in single-tenant dev corpus. |
| `visibility` | enum | One of: `public_internal`, `team`, `restricted`, `confidential`. Coarse access label applied at source level. |
| `allowed_roles` | string[] | Roles permitted to read evidence from this source. Empty array means role check is not used at source level. |
| `allowed_groups` | string[] | Groups permitted to read evidence from this source. Empty array means group check is not used at source level. |
| `sensitivity` | enum | One of: `low`, `medium`, `high`. Used for reporting and future policy rules. |
| `registered_at` | ISO 8601 datetime | When the source was registered. |
| `freshness_as_of` | ISO 8601 datetime | Last known content update or export time for the source corpus. |
| `freshness_policy` | enum | One of: `static`, `periodic_export`, `live_sync`. Describes how freshness is maintained. |
| `uri` | string | Canonical location or export path reference (not necessarily fetchable in Phase 1). |
| `citation_label` | string | Short label used in citation output, e.g. "Security Policy Handbook v3". |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `policy_tags` | string[] | Tags for future policy-aware filtering, e.g. `pii`, `legal_hold`. |
| `language` | string | BCP 47 language tag, default `en`. |
| `description` | string | Short description of source contents and intended use. |
| `parent_source_id` | string | If this source is a partition of a larger source. |
| `version` | string | Source version or export batch identifier. |
| `contact_id` | string | Escalation contact for source quality issues. |

## Permission Semantics

Access decision at source level uses this order:

1. If `tenant_id` on the requester context does not match source `tenant_id`, deny.
2. If requester has a role in `allowed_roles` when that list is non-empty, allow.
3. Else if requester has a group in `allowed_groups` when that list is non-empty, allow.
4. Else apply `visibility` rules defined in the permission test matrix (Phase 6).

Document-level permissions may further restrict access but must not widen beyond source-level scope.

## Freshness Semantics

- `freshness_as_of` is the authoritative "content current as of" timestamp for evaluation and citation display.
- `freshness_policy` documents how the timestamp is expected to change:
  - `static`: corpus snapshot; timestamp set at registration.
  - `periodic_export`: updated on each export cycle.
  - `live_sync`: reserved for future connector work; not used in first corpus.

Retrieval may surface freshness in candidate and citation records but must not infer freshness from file mtimes alone.

## Citation Requirements

Every source must provide enough data to produce a citation header without reading document body:

- `source_id`
- `citation_label` (or `title` if label omitted)
- `uri` (for audit, may be redacted in output for restricted requesters)
- `freshness_as_of`

## Registration Validation Rules

A source record is **invalid** if:

- `source_id` is missing or duplicates an existing registration
- `tenant_id`, `owner_id`, or `visibility` is missing
- `freshness_as_of` or `registered_at` is missing
- both `allowed_roles` and `allowed_groups` are absent when `visibility` is `team` or `restricted`

Invalid records must not be used for ingestion.

## Relationship To Downstream Records

| Downstream record | Must copy from source |
|-------------------|----------------------|
| Document record | `source_id`, `tenant_id`, `owner_id`, `visibility`, `allowed_roles`, `allowed_groups`, `sensitivity`, `freshness_as_of`, `citation_label` |
| Chunk record | `source_id`, `tenant_id`, permission fields, `freshness_as_of` |
| Retrieval candidate | `source_id`, permission decision, citation reference fields |

## Example Records

See [ingestion-contract.md](ingestion-contract.md) for full source registration examples tied to the first corpus.

## Open Decisions

- Whether document-level permission overrides are required for the first corpus (default: inherit from source unless explicitly overridden).
- Whether `uri` should be redacted in citation output for `confidential` visibility (default: yes for limited requesters).

## Next Steps

1. Review examples in `docs/ingestion-contract.md`.
2. Confirm first corpus sources in `docs/first-corpus-plan.md`.
3. After review approval, allow minimal source registry implementation (Phase 1 optional output).
