# Ingestion Contract

## Purpose

Define how raw markdown becomes normalized `DocumentRecord` instances while preserving source identity and permission metadata.

## DocumentRecord Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `document_id` | string | yes | Stable ID, e.g. `DOC-{source_id}` |
| `source_id` | string | yes | Parent source reference |
| `title` | string | yes | Document title |
| `format` | string | yes | e.g. `markdown` |
| `content_hash` | string | yes | SHA256 of normalized body |
| `content_path` | string | yes | Path to source file |
| `ingested_at` | ISO8601 | yes | Ingestion timestamp |
| `byte_size` | int | yes | File size in bytes |
| `permission_inherit` | bool | yes | Default `true` |
| `visibility_override` | enum | no | Override source visibility |
| `metadata` | object | no | Extra key-value metadata |

## Ingestion Boundaries

1. YAML frontmatter in markdown supplies source-level permission fields.
2. Body text is stored separately; hash computed on normalized body (trimmed).
3. Ingestion does not chunk; chunking is Phase 2.
4. Anonymous ingestion (no `source_id`) is rejected.

## Example DocumentRecord

```json
{
  "document_id": "DOC-SRC-api-auth",
  "source_id": "SRC-api-auth",
  "title": "API Authentication Specification",
  "format": "markdown",
  "content_hash": "a1b2c3...",
  "content_path": "corpus/sources/api-authentication-spec.md",
  "ingested_at": "2026-06-01T12:00:00Z",
  "byte_size": 4521,
  "permission_inherit": true,
  "metadata": {}
}
```
