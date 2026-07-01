# Source Registration Contract

## Purpose

Define required fields for `SourceRecord` before ingestion or retrieval code runs.

## SourceRecord Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source_id` | string | yes | Stable identifier, e.g. `SRC-security-policy` |
| `title` | string | yes | Human-readable source title |
| `source_type` | string | yes | e.g. `markdown`, `policy`, `runbook` |
| `uri` | string | yes | Path or URI to raw content |
| `owner_id` | string | yes | Owning team or user |
| `tenant_id` | string | yes | Tenant scope, default `tenant-default` |
| `visibility` | enum | yes | `public`, `general`, `internal`, `hr-only`, `confidential`, `legal` |
| `allowed_roles` | string[] | yes | Roles permitted to access; empty = deny all |
| `allowed_groups` | string[] | no | Optional group-based access |
| `sensitivity` | string | yes | e.g. `low`, `medium`, `high`, `critical` |
| `policy_tags` | string[] | no | e.g. `pii`, `security`, `finance` |
| `freshness_updated_at` | ISO8601 | yes | Last content update timestamp |
| `registered_at` | ISO8601 | yes | Registration timestamp |
| `citation_display_name` | string | yes | Short label for citations |

## Rules

1. Every ingested document must reference a registered `source_id`.
2. Permission metadata must not be stripped at registration.
3. Missing `visibility` or `allowed_roles` at chunk time → deny-by-default.
4. `source_id` is immutable once registered.

## Example

```json
{
  "source_id": "SRC-api-auth",
  "title": "API Authentication Specification",
  "source_type": "markdown",
  "uri": "corpus/sources/api-authentication-spec.md",
  "owner_id": "team-platform",
  "tenant_id": "tenant-default",
  "visibility": "internal",
  "allowed_roles": ["engineer", "admin", "security"],
  "allowed_groups": [],
  "sensitivity": "medium",
  "policy_tags": ["security"],
  "freshness_updated_at": "2026-01-15T00:00:00Z",
  "registered_at": "2026-06-01T00:00:00Z",
  "citation_display_name": "API Auth Spec"
}
```
