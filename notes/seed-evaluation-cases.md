# Seed Evaluation Cases

**Phase:** 9 prep (usable from Phase 1 onward)  
**Corpus:** See `docs/first-corpus-plan.md`  
**Purpose:** Initial query cases for lexical baseline and permission evaluation before implementation exists.

These cases use the schema defined in `docs/evaluation-plan.md`. Expected chunk IDs are provisional until Phase 2 chunking assigns stable chunk identifiers.

## Case Index

| Case ID | Category | Primary test |
|---------|----------|--------------|
| `case-001` | lexical_exact | Exact policy term match |
| `case-002` | lexical_exact | Exact identifier / number |
| `case-003` | semantic_paraphrase | Paraphrased policy intent |
| `case-004` | permission_allow | Employee access to public policy |
| `case-005` | permission_deny | Employee blocked from HR data |
| `case-006` | permission_partial | Oncall access to runbooks only |
| `case-007` | permission_no_access | Requester with no roles |
| `case-008` | cross_source | Query spanning allowed sources for persona |
| `case-009` | no_result | Evidence does not exist in corpus |
| `case-010` | ranking_setup | Multiple relevant docs; ranking order matters |

---

## case-001

```yaml
case_id: case-001
query_text: "What is the minimum password length?"
requester:
  persona_id: user:employee
  tenant_id: tenant:acme
  roles: [employee]
  groups: []
expected_relevant:
  documents: [corp:policy-handbook:password-policy]
  chunks: []  # assign after Phase 2 chunking
expected_inaccessible: []
acceptable_alternates: []
required_citation_behavior: Must cite Security Policy Handbook password section.
permission_expectation: allow
primary_metric: recall@3
notes: Exact-term query; lexical baseline should succeed.
failure_category_if_known: null
```

## case-002

```yaml
case_id: case-002
query_text: "E4 compensation salary range"
requester:
  persona_id: user:hr-admin
  tenant_id: tenant:acme
  roles: [hr_admin]
  groups: [group:hr-leads]
expected_relevant:
  documents: [corp:hr-compensation:band-levels]
  chunks: []
expected_inaccessible: []
acceptable_alternates: []
required_citation_behavior: Must cite HR Compensation Guide band table.
permission_expectation: allow
primary_metric: recall@1
notes: Exact identifier and numeric range; tests precise term retrieval.
failure_category_if_known: null
```

## case-003

```yaml
case_id: case-003
query_text: "How should staff authenticate when working remotely?"
requester:
  persona_id: user:employee
  tenant_id: tenant:acme
  roles: [employee]
  groups: []
expected_relevant:
  documents:
    - corp:policy-handbook:password-policy
    - corp:policy-handbook:remote-work
  chunks: []
expected_inaccessible: []
acceptable_alternates:
  - corp:policy-handbook:password-policy  # if remote-work chunk weak
required_citation_behavior: At least one citation from policy handbook.
permission_expectation: allow
primary_metric: recall@3
notes: Paraphrase query; semantic baseline should help over pure keyword match.
failure_category_if_known: null
```

## case-004

```yaml
case_id: case-004
query_text: "MFA requirements for VPN"
requester:
  persona_id: user:employee
  tenant_id: tenant:acme
  roles: [employee]
  groups: []
expected_relevant:
  documents: [corp:policy-handbook:password-policy]
  chunks: []
expected_inaccessible: []
acceptable_alternates: []
required_citation_behavior: Citation must be from allowed source only.
permission_expectation: allow
primary_metric: allowed_recall@3
notes: Permission allow control case for public_internal source.
failure_category_if_known: null
```

## case-005

```yaml
case_id: case-005
query_text: "E5 compensation band range"
requester:
  persona_id: user:employee
  tenant_id: tenant:acme
  roles: [employee]
  groups: []
expected_relevant:
  documents: [corp:hr-compensation:band-levels]
  chunks: []
expected_inaccessible:
  documents: [corp:hr-compensation:band-levels]
  chunks: []
acceptable_alternates: []
required_citation_behavior: No HR citation should appear in output for this requester.
permission_expectation: deny
primary_metric: unauthorized_evidence_in_top_k
notes: Relevant evidence exists globally but must not appear for employee. Zero unauthorized leakage is required.
failure_category_if_known: permission_false_allow
```

## case-006

```yaml
case_id: case-006
query_text: "incident commander assignment steps"
requester:
  persona_id: user:platform-oncall
  tenant_id: tenant:acme
  roles: [employee]
  groups: [group:platform-eng, group:oncall]
expected_relevant:
  documents: [corp:eng-runbooks:incident-response]
  chunks: []
expected_inaccessible:
  documents: [corp:hr-compensation:band-levels]
  chunks: []
acceptable_alternates: []
required_citation_behavior: Cite runbook; must not leak HR titles or paths.
permission_expectation: allow
primary_metric: allowed_recall@3
notes: Team-scoped allow; ensures group-based access works and restricted docs stay out.
failure_category_if_known: null
```

## case-007

```yaml
case_id: case-007
query_text: "password rotation policy"
requester:
  persona_id: user:no-access
  tenant_id: tenant:acme
  roles: []
  groups: []
expected_relevant:
  documents: [corp:policy-handbook:password-policy]
  chunks: []
expected_inaccessible:
  documents: [corp:policy-handbook:password-policy]
  chunks: []
acceptable_alternates: []
required_citation_behavior: Empty or explicit no-access result; no citations.
permission_expectation: deny
primary_metric: unauthorized_evidence_in_top_k
notes: Requester lacks required roles; system should distinguish no access from no evidence.
failure_category_if_known: null
```

## case-008

```yaml
case_id: case-008
query_text: "deploy rollback procedure after failed release"
requester:
  persona_id: user:platform-oncall
  tenant_id: tenant:acme
  roles: [employee]
  groups: [group:platform-eng, group:oncall]
expected_relevant:
  documents: [corp:eng-runbooks:deploy-rollback]
  chunks: []
expected_inaccessible: []
acceptable_alternates: [corp:eng-runbooks:incident-response]
required_citation_behavior: Cite deploy rollback runbook as primary evidence.
permission_expectation: allow
primary_metric: recall@3
notes: Procedural query within team-allowed source.
failure_category_if_known: null
```

## case-009

```yaml
case_id: case-009
query_text: "pet insurance reimbursement policy"
requester:
  persona_id: user:employee
  tenant_id: tenant:acme
  roles: [employee]
  groups: []
expected_relevant:
  documents: []
  chunks: []
expected_inaccessible: []
acceptable_alternates: []
required_citation_behavior: No citation; explicit no-evidence result preferred over hallucinated match.
permission_expectation: allow
primary_metric: no_result_rate
notes: Source gap / no evidence case. Distinguish from permission deny.
failure_category_if_known: source_gap
```

## case-010

```yaml
case_id: case-010
query_text: "data classification labels for customer PII"
requester:
  persona_id: user:employee
  tenant_id: tenant:acme
  roles: [employee]
  groups: []
expected_relevant:
  documents: [corp:policy-handbook:data-classification]
  chunks: []
expected_inaccessible: []
acceptable_alternates:
  - corp:policy-handbook:password-policy  # lower relevance
required_citation_behavior: Primary citation should be data classification section.
permission_expectation: allow
primary_metric: mean_reciprocal_rank
notes: Multiple handbook docs may match weakly; ranking quality matters.
failure_category_if_known: ranking_failure
```

## Usage Notes

- Assign `chunks` after Phase 2 chunking stabilizes boundaries.
- Run permission cases (005, 006, 007) on every retrieval change once filtering exists.
- Keep this file updated when documents are added to `docs/first-corpus-plan.md`.
