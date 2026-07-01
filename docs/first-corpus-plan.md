# First Corpus Plan

**Phase:** 1  
**Status:** Draft for review  
**Purpose:** Choose the initial source set for evaluation and early retrieval experiments.

## Selection Criteria

The first corpus must be:

1. **Small** — manageable by hand for gold evaluation cases.
2. **Permission-diverse** — includes public-internal, team-scoped, and restricted sources.
3. **Citation-friendly** — clear sections and stable titles for chunk and citation design.
4. **Retrieval-varied** — supports exact-term, paraphrase, and cross-source queries.
5. **Static** — snapshot-based (`freshness_policy: static` or `periodic_export`) to avoid connector work.

## Proposed Sources

| Source ID | Type | Visibility | Purpose in evaluation |
|-----------|------|------------|------------------------|
| `corp:policy-handbook` | policy_doc | public_internal | Exact policy terms, broad employee access |
| `corp:hr-compensation` | policy_doc | restricted | Permission deny and allowed-recall separation |
| `corp:eng-runbooks` | runbook | team | Team/group-scoped access, procedural queries |

**Tenant:** `tenant:acme` (single-tenant synthetic enterprise)

**Estimated document count:** 8–12 documents total across three sources (2–4 documents per source).

## Planned Documents By Source

### corp:policy-handbook

| Document ID | Topic |
|-------------|-------|
| `corp:policy-handbook:password-policy` | Password length, MFA, rotation |
| `corp:policy-handbook:data-classification` | Data sensitivity labels |
| `corp:policy-handbook:remote-work` | Remote access requirements |

### corp:hr-compensation

| Document ID | Topic |
|-------------|-------|
| `corp:hr-compensation:band-levels` | Engineering band ranges |
| `corp:hr-compensation:bonus-policy` | Bonus eligibility rules |

### corp:eng-runbooks

| Document ID | Topic |
|-------------|-------|
| `corp:eng-runbooks:incident-response` | Incident steps and timelines |
| `corp:eng-runbooks:deploy-rollback` | Deployment rollback procedure |
| `corp:eng-runbooks:oncall-handoff` | Oncall handoff checklist |

## Requester Personas For Evaluation

| Persona ID | Roles | Groups | Intended access |
|------------|-------|--------|-----------------|
| `user:employee` | `employee` | — | policy handbook only |
| `user:platform-oncall` | `employee` | `group:platform-eng`, `group:oncall` | handbook + runbooks |
| `user:hr-admin` | `hr_admin` | `group:hr-leads` | handbook + HR compensation |
| `user:contractor-ext` | `contractor` | — | handbook only (same as employee for first corpus) |
| `user:no-access` | — | — | deny all sources |

## Why Not More Sources Yet

- Ticket exports and live wiki sync add ingestion complexity without improving Phase 1 contract clarity.
- A larger corpus makes gold labeling expensive before chunking strategy exists.
- Additional source types can be added after Phase 2 chunking baseline is chosen.

## Corpus Format

- Files stored as markdown under a future `corpus/` directory (Phase 1 optional implementation or Phase 2 prep).
- File content must match example records in `docs/ingestion-contract.md`.
- Registration records remain the authority for permission metadata even if file headers also contain titles.

## Freshness Representation

For the first corpus:

- All sources use explicit `freshness_as_of` timestamps in registration records.
- `corp:eng-runbooks` uses `freshness_policy: periodic_export` to exercise freshness display; others use `static`.
- Retrieval must not infer freshness from filesystem metadata alone.

## Exit Criteria

- [x] Source types selected
- [x] Permission diversity confirmed across three sources
- [x] Document inventory listed with stable IDs
- [x] Requester personas defined for evaluation

## Next Steps

1. Create markdown corpus files when moving to Phase 2 or minimal ingestion implementation.
2. Align seed evaluation cases in `notes/seed-evaluation-cases.md` with this inventory.
3. Revisit corpus size after chunking baseline produces boundary examples.
