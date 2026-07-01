# Seed Evaluation Cases

Phase: 9 (seed set for Phases 3–7)

## Schema

Each case includes: `case_id`, `query`, `requester_id`, `expected_chunk_ids` or `expected_source_ids`, `expected_inaccessible`, `method`, `notes`.

## Seed Cases (10)

### LEX-01
- query: `API token rotation procedure`
- requester: `admin_full`
- expected_source_ids: [`SRC-api-auth`]
- method: lexical
- notes: Exact terminology match

### LEX-02
- query: `expense reimbursement receipt deadline`
- requester: `hr_manager`
- expected_source_ids: [`SRC-expense-policy`]
- method: lexical

### LEX-03
- query: `P0 incident escalation`
- requester: `admin_full`
- expected_source_ids: [`SRC-incident-runbook`]
- method: lexical

### LEX-04
- query: `coding standards pull request review`
- requester: `engineer_std`
- expected_source_ids: [`SRC-coding-standards`]
- method: lexical

### SEM-01
- query: `how to prove identity when calling our HTTP APIs`
- requester: `engineer_std`
- expected_source_ids: [`SRC-api-auth`]
- method: semantic
- notes: Paraphrase of authentication

### SEM-02
- query: `working from home equipment policy`
- requester: `engineer_std`
- expected_source_ids: [`SRC-remote-work`]
- method: semantic

### SEM-03
- query: `new hire first week checklist`
- requester: `hr_manager`
- expected_source_ids: [`SRC-onboarding`]
- method: semantic

### SEM-04
- query: `roadmap themes for next quarter`
- requester: `engineer_std`
- expected_source_ids: [`SRC-product-roadmap`]
- method: semantic

### PERM-01
- query: `data encryption at rest requirements`
- requester: `engineer_std`
- expected_source_ids: [`SRC-security-policy`]
- expected_inaccessible: true
- method: hybrid
- notes: Relevant but denied for engineer

### PERM-02
- query: `remote work core hours`
- requester: `contractor_limited`
- expected_source_ids: [`SRC-remote-work`]
- method: hybrid
- notes: Only allowed source for contractor
