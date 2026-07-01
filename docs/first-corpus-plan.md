# First Corpus Plan

## Purpose

Define the markdown corpus for retrieval, permission, and citation evaluation.

## Corpus Files (12)

| # | source_id | File | Topic | visibility | allowed_roles |
|---|-----------|------|-------|------------|---------------|
| 1 | SRC-security-policy | security-data-handling-policy.md | Data classification, encryption | confidential | admin, security |
| 2 | SRC-incident-runbook | incident-response-runbook.md | Incident response | confidential | admin, security, engineer |
| 3 | SRC-api-auth | api-authentication-spec.md | API authentication | internal | engineer, admin, security |
| 4 | SRC-coding-standards | engineering-coding-standards.md | Coding standards | internal | engineer, admin |
| 5 | SRC-product-roadmap | quarterly-product-roadmap.md | Product roadmap | internal | engineer, product, admin |
| 6 | SRC-onboarding | employee-onboarding-guide.md | Onboarding | hr-only | hr, admin |
| 7 | SRC-expense-policy | expense-reimbursement-policy.md | Expense reimbursement | hr-only | hr, admin |
| 8 | SRC-remote-work | remote-work-guidelines.md | Remote work | general | engineer, hr, support, admin, product |
| 9 | SRC-support-playbook | customer-support-playbook.md | Support playbook | internal | support, admin |
| 10 | SRC-vendor-access | vendor-access-agreement-summary.md | Vendor access | legal | admin, legal |
| 11 | SRC-data-retention | data-retention-policy.md | Data retention | internal | admin, legal, engineer |
| 12 | SRC-platform-sla | platform-sla-overview.md | Platform SLA | internal | engineer, admin, product |

## Eval Extension

4 additional cases in `eval/cases/ext.yaml` (EXT-01..04) cover sources 11–12.

## Status

Implemented. Manifest: `corpus/manifest.yaml`.
