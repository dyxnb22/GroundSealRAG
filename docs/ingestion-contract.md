# Ingestion Contract

**Phase:** 1  
**Status:** Draft for review  
**Purpose:** Define how raw content becomes normalized document records while preserving source identity, permission metadata, and citation fields.

## Scope

This contract covers:

- normalized **document records** produced by ingestion
- non-executable **example records** for review
- ingestion boundaries and assumptions

It does not define chunking (Phase 2) or retrieval behavior (Phase 3+).

## Ingestion Pipeline (Conceptual)

```mermaid
flowchart LR
    SR[Registered Source] --> RAW[Raw Content]
    RAW --> NORM[Normalization]
    NORM --> DOC[Document Record]
    DOC --> CHK[Chunking Phase 2]
```

Ingestion must not produce documents without a valid registered source.

## Document Record Schema

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `document_id` | string | Stable unique ID within source, e.g. `corp:policy-handbook:sec-004`. |
| `source_id` | string | Reference to registered source. |
| `title` | string | Document title for citation and display. |
| `body_text` | string | Normalized plain text or structured text representation. |
| `content_hash` | string | Hash of normalized body for change detection. |
| `tenant_id` | string | Copied from source; must match. |
| `owner_id` | string | Copied from source unless document-level override is defined. |
| `visibility` | enum | Same enum as source contract. |
| `allowed_roles` | string[] | Copied or narrowed from source. |
| `allowed_groups` | string[] | Copied or narrowed from source. |
| `sensitivity` | enum | Copied from source unless overridden. |
| `freshness_as_of` | ISO 8601 datetime | Copied from source or updated if document has independent freshness. |
| `ingested_at` | ISO 8601 datetime | When normalization completed. |
| `structure` | object | Lightweight structure hints: headings, sections, page breaks. |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `section_path` | string | Logical path within source, e.g. `Security > Access Control`. |
| `external_ref` | string | Original file name, ticket ID, or wiki page ID. |
| `language` | string | BCP 47 tag if different from source default. |
| `permission_override` | boolean | True if document permissions are narrower than source. |

## Ingestion Rules

1. **No anonymous ingestion** — reject content without `source_id`.
2. **Permission inheritance** — copy permission fields from source; document may narrow but not widen access.
3. **Structure preservation** — retain heading boundaries in `structure` to support Phase 2 chunking.
4. **Stable IDs** — `document_id` must remain stable across re-ingestion when content is unchanged.
5. **Change detection** — update `content_hash` and optionally `freshness_as_of` when body changes.
6. **Citation readiness** — every document must be citeable via `document_id`, `source_id`, and `title`.

## Normalization Assumptions (First Corpus)

| Source type | Normalization approach |
|-------------|------------------------|
| `policy_doc` | Markdown or plain text; headings become structure entries. |
| `internal_wiki` | HTML or markdown stripped to text; preserve heading hierarchy. |
| `runbook` | Step lists preserved as structured list nodes in `structure`. |
| `faq` | Each Q/A pair may become a separate document with shared `source_id`. |

## Example Source Registration Records

### Example 1: Security Policy Handbook

```json
{
  "source_id": "corp:policy-handbook",
  "source_type": "policy_doc",
  "title": "Corporate Security Policy Handbook",
  "owner_id": "team:security",
  "tenant_id": "tenant:acme",
  "visibility": "public_internal",
  "allowed_roles": ["employee", "contractor"],
  "allowed_groups": [],
  "sensitivity": "medium",
  "registered_at": "2026-06-01T10:00:00Z",
  "freshness_as_of": "2026-05-15T08:00:00Z",
  "freshness_policy": "static",
  "uri": "file://corpus/policy-handbook-v3.md",
  "citation_label": "Security Policy Handbook v3",
  "policy_tags": ["security", "compliance"],
  "language": "en",
  "version": "3.0"
}
```

### Example 2: HR Confidential Compensation Guide

```json
{
  "source_id": "corp:hr-compensation",
  "source_type": "policy_doc",
  "title": "Compensation and Bands Guide",
  "owner_id": "team:hr",
  "tenant_id": "tenant:acme",
  "visibility": "restricted",
  "allowed_roles": ["hr_admin", "exec"],
  "allowed_groups": ["group:hr-leads"],
  "sensitivity": "high",
  "registered_at": "2026-06-01T10:00:00Z",
  "freshness_as_of": "2026-04-01T08:00:00Z",
  "freshness_policy": "static",
  "uri": "file://corpus/hr-compensation-guide.md",
  "citation_label": "HR Compensation Guide",
  "policy_tags": ["pii", "hr"],
  "language": "en",
  "version": "1.2"
}
```

### Example 3: Engineering Runbooks

```json
{
  "source_id": "corp:eng-runbooks",
  "source_type": "runbook",
  "title": "Platform Engineering Runbooks",
  "owner_id": "team:platform",
  "tenant_id": "tenant:acme",
  "visibility": "team",
  "allowed_roles": [],
  "allowed_groups": ["group:platform-eng", "group:oncall"],
  "sensitivity": "medium",
  "registered_at": "2026-06-01T10:00:00Z",
  "freshness_as_of": "2026-06-20T14:00:00Z",
  "freshness_policy": "periodic_export",
  "uri": "file://corpus/runbooks/",
  "citation_label": "Platform Runbooks",
  "language": "en",
  "version": "2026-06-export"
}
```

## Example Document Records

### Example D1: Password Policy Section

```json
{
  "document_id": "corp:policy-handbook:password-policy",
  "source_id": "corp:policy-handbook",
  "title": "Password and Authentication Policy",
  "body_text": "All employees must use passwords of at least 14 characters. Multi-factor authentication is required for VPN and admin systems. Passwords must be rotated every 90 days for privileged accounts.",
  "content_hash": "sha256:a1b2c3example",
  "tenant_id": "tenant:acme",
  "owner_id": "team:security",
  "visibility": "public_internal",
  "allowed_roles": ["employee", "contractor"],
  "allowed_groups": [],
  "sensitivity": "medium",
  "freshness_as_of": "2026-05-15T08:00:00Z",
  "ingested_at": "2026-06-01T11:00:00Z",
  "structure": {
    "headings": [
      {"level": 1, "text": "Password and Authentication Policy", "offset": 0}
    ]
  },
  "section_path": "Security > Authentication",
  "external_ref": "policy-handbook-v3.md#password-policy"
}
```

### Example D2: Compensation Band Table (Restricted)

```json
{
  "document_id": "corp:hr-compensation:band-levels",
  "source_id": "corp:hr-compensation",
  "title": "Engineering Compensation Bands",
  "body_text": "Level E4 base compensation range: 180000-220000 USD. Level E5 base compensation range: 220000-280000 USD. Bands effective fiscal year 2026.",
  "content_hash": "sha256:d4e5f6example",
  "tenant_id": "tenant:acme",
  "owner_id": "team:hr",
  "visibility": "restricted",
  "allowed_roles": ["hr_admin", "exec"],
  "allowed_groups": ["group:hr-leads"],
  "sensitivity": "high",
  "freshness_as_of": "2026-04-01T08:00:00Z",
  "ingested_at": "2026-06-01T11:05:00Z",
  "structure": {
    "headings": [
      {"level": 2, "text": "Engineering Compensation Bands", "offset": 0}
    ]
  },
  "section_path": "Compensation > Engineering",
  "external_ref": "hr-compensation-guide.md#engineering-bands",
  "permission_override": false
}
```

### Example D3: Incident Response Runbook

```json
{
  "document_id": "corp:eng-runbooks:incident-response",
  "source_id": "corp:eng-runbooks",
  "title": "Incident Response Runbook",
  "body_text": "Step 1: Acknowledge alert in PagerDuty within 5 minutes. Step 2: Open incident channel #incident-YYYYMMDD. Step 3: Assign incident commander. Step 4: Document timeline in incident log.",
  "content_hash": "sha256:g7h8i9example",
  "tenant_id": "tenant:acme",
  "owner_id": "team:platform",
  "visibility": "team",
  "allowed_roles": [],
  "allowed_groups": ["group:platform-eng", "group:oncall"],
  "sensitivity": "medium",
  "freshness_as_of": "2026-06-20T14:00:00Z",
  "ingested_at": "2026-06-21T09:00:00Z",
  "structure": {
    "headings": [
      {"level": 1, "text": "Incident Response Runbook", "offset": 0}
    ],
    "lists": [
      {"type": "ordered", "start_offset": 0, "items": 4}
    ]
  },
  "section_path": "Runbooks > Incident Response",
  "external_ref": "runbooks/incident-response.md"
}
```

## Ingestion Failure Modes

| Failure | Handling |
|---------|----------|
| Unknown `source_id` | Reject ingestion; log source gap failure. |
| Missing permission fields on source | Block ingestion until source record is fixed. |
| Empty body | Reject document; do not create placeholder chunks later. |
| Unstable external IDs | Require mapping table before re-ingestion. |
| Widened permissions at document level | Reject override; log metadata gap failure. |

## Exit Criteria (Phase 1 Document Portion)

- [x] Source metadata fields defined in `docs/source-registration-contract.md`
- [x] Document record fields defined
- [x] Non-executable example records provided
- [x] Ingestion boundaries and failure modes documented

## Next Steps

1. Confirm corpus files align with examples in `docs/first-corpus-plan.md`.
2. Begin Phase 2 chunk record contract using `structure` hints from document records.
3. After contract review, implement minimal source registry (Phase 1 optional).
