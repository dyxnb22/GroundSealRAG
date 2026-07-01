---
source_id: SRC-coding-standards
title: Engineering Coding Standards
owner_id: team-engineering
visibility: internal
allowed_roles: [engineer, admin]
sensitivity: low
freshness_updated_at: "2026-03-01T00:00:00Z"
---

# Engineering Coding Standards

These standards define consistent code quality, review practices, and style expectations for all GroundSeal engineering repositories. They apply to application code, infrastructure definitions, data pipelines, and internal tools. Adherence is required before merge to protected branches.

## Goals

Consistent coding standards reduce defect rates, shorten onboarding time, and make ownership transfers predictable. Reviews should focus on correctness, security, operability, and maintainability rather than personal preference when a rule is documented here.

## Repository Conventions

Each repository includes a README with setup instructions, architecture overview, and ownership contacts. Protected branches require passing CI checks and at least one approved review unless emergency procedures apply.

Use conventional commits or equivalent structured messages. Link tickets in pull request descriptions. Keep changes scoped; unrelated refactors belong in separate pull requests.

## Code Style

Style rules prioritize readability and diff clarity over brevity.

**General code style expectations:**

- Format code using the repository's configured formatter; do not hand-format to bypass automation.
- Prefer explicit names over abbreviations except widely understood domain terms.
- Functions and methods should do one thing; extract helpers when logic branches exceed reasonable depth.
- Avoid commented-out code in merged commits; use version control history instead.
- Handle errors explicitly; do not swallow exceptions without logging context.
- Add types in typed languages for public interfaces and cross-module boundaries.
- Limit file length; split modules when cohesion breaks down.

Language-specific linters run in CI. Suppressions require inline justification comments and reviewer acknowledgment.

## Testing Expectations

Features include automated tests proportional to risk. Bug fixes include regression tests when feasible. Flaky tests are treated as production defects and quarantined until fixed.

Integration tests cover critical paths. Load and chaos testing are required before major release milestones documented in the product roadmap.

## Pull Request Review

Pull request review is the primary quality gate before code reaches production. Authors request review from domain owners and at least one engineer unfamiliar with the change when risk is high.

**Coding standards pull request review checklist:**

- Verify the change matches the ticket scope and design discussion.
- Confirm tests exist, pass in CI, and cover new behavior or bug fixes.
- Read for security issues: injection, auth bypass, secret leakage, and unsafe deserialization.
- Check observability: metrics, logs, and traces for new failure modes.
- Assess performance and resource usage for hot paths and data growth.
- Validate configuration defaults are safe and documented.
- Ensure migrations and rollbacks are reversible or have a documented forward-only plan.
- Confirm naming, structure, and comments follow this coding standards document.

Reviewers leave actionable comments and distinguish blocking issues from suggestions. Authors respond to all comments before merge. Approval means the reviewer would maintain the code comfortably.

Turnaround target is one business day for standard reviews. Urgent production fixes use the hotfix lane with post-merge review within twenty-four hours.

## Security and Secrets

Never commit secrets, tokens, or private keys. Use environment injection and the secrets manager. Depend on automated dependency scanning and patch critical vulnerabilities within SLA defined by security.

## Documentation in Code

Public APIs require docstrings or equivalent reference documentation. Complex algorithms include brief comments explaining invariants. README and runbook links are updated when operational behavior changes.

## Performance and Reliability

Avoid premature optimization but address known N+1 queries, unbounded memory growth, and missing timeouts. External calls use deadlines and retries with jitter. Feature flags isolate risky launches.

## Infrastructure and Data Code

Infrastructure as code follows the same review standards as application code. Plans are attached to pull requests for production-impacting changes. Database schema changes include backward-compatible phases when zero-downtime is required.

## Deprecation and Removal

Mark deprecated APIs with timeline and replacement. Remove dead code when usage reaches zero in metrics. Large deletions still require review for hidden dependencies.

## Enforcement

CI enforces formatters, linters, and test thresholds. Repeated style debates should result in rule updates here rather than ad hoc enforcement in each pull request. Teams that bypass required checks without documented emergency approval receive repo configuration audits from platform engineering.

## Onboarding for New Engineers

New hires should read this document during their first week checklist before opening production-impacting pull requests. Buddies verify understanding by walking through a sample pull request review on a low-risk change so authors learn where to request review and how to respond to blocking feedback constructively.

## Version Control Practices

Use feature branches named with ticket identifiers. Rebase or merge according to team convention documented in repository README. Squash commits when they represent a single logical change unless history is needed for audit. Never force-push to shared branches without team agreement.

## Standards Maintenance

Engineering leadership owns this document. Teams propose amendments through RFC pull requests to the standards repository. Updates take effect on merge unless a grace period is announced. Major revisions trigger a short lunch-and-learn so pull request review expectations stay synchronized across repositories.
