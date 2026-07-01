---
source_id: SRC-platform-sla
title: Platform SLA Overview
owner_id: team-platform
visibility: internal
allowed_roles: [engineer, admin, product]
sensitivity: medium
freshness_updated_at: "2026-03-01T00:00:00Z"
---

# Platform SLA Overview

This document summarizes service level commitments for the GroundSeal platform, including availability targets, incident response expectations, and planned maintenance practices. It is intended for engineers, product managers, and administrators configuring customer-facing commitments. External customer contracts may specify additional terms; refer to executed agreements when they differ from this internal overview.

## Service Scope

The platform SLA applies to production-hosted APIs, authentication services, core data ingestion pipelines, and the customer admin console served from GroundSeal-operated regions. It excludes customer-managed integrations, beta features marked as preview, and third-party networks outside GroundSeal control.

Each production region is measured independently unless a global incident affects multiple regions. Sandbox and development environments are best-effort and excluded from formal commitments.

## Platform Uptime SLA

GroundSeal commits to a **platform uptime SLA** measured monthly for each covered production service. Uptime equals total minutes in the month minus downtime minutes, divided by total minutes in the month.

**Downtime** is sustained unavailability of a covered API endpoint or console login path, confirmed by external synthetic checks and internal monitoring, lasting five consecutive minutes or longer. Partial degradation that preserves authenticated read access may be classified separately unless error rates exceed defined thresholds.

The **platform uptime SLA** target for standard production tiers is **99.9% availability**, equivalent to approximately forty-three minutes of allowable downtime per thirty-day month. Enterprise tier customers may receive higher targets documented in order forms.

Exclusions from downtime calculations include scheduled **maintenance window** periods announced at least seventy-two hours in advance, force majeure events, upstream provider outages documented in status communications, and customer-caused misconfiguration. Credit calculations for qualifying downtime follow the commercial credit schedule in customer agreements.

## Availability Targets by Component

Availability targets translate the overall **platform uptime SLA** into component-level objectives used by engineering for error budgets and release gating.

| Component | Monthly target | Measurement method |
|-----------|----------------|--------------------|
| Public REST API (core) | 99.9% | Regional synthetic probes plus gateway success rate |
| Authentication and token issuance | 99.95% | Auth service health checks and login success rate |
| Admin console | 99.9% | Browser synthetic transactions |
| Batch ingestion pipeline | 99.5% | Job completion within published SLA window |
| Search and retrieval API | 99.9% | Query success rate excluding client timeouts |

Error budgets are tracked in the platform reliability dashboard. When a service consumes more than fifty percent of its monthly error budget before the fifteenth calendar day, feature freeze rules apply to non-critical releases until recovery is demonstrated.

## Incident Response Time

Incident response time commitments define how quickly GroundSeal acknowledges and engages on production issues affecting covered services. These expectations complement severity definitions in the Incident Response Runbook.

**Initial response targets:**

- **P0 (critical outage or confirmed data exposure):** Acknowledge within five minutes; incident commander within fifteen minutes; status page update within fifteen minutes when customers are affected.
- **P1 (major degradation):** Acknowledge within ten minutes; incident commander within thirty minutes.
- **P2 (partial impact with workaround):** Acknowledge within thirty minutes; assigned owner within two hours during business hours.
- **P3 (minor or internal-only):** Acknowledge within four business hours.

**Communication cadence during impact:**

- P0: Customer-facing updates at least every thirty minutes until impact ends.
- P1: Updates at least every sixty minutes during customer-visible impact.
- P2 and P3: Updates at incident closure unless stakeholders request interim notes.

On-call rotations cover twenty-four hours a day for P0 and P1 pathways. Incident response time metrics are reported monthly, including time to acknowledge, time to mitigate, and time to resolve.

## Maintenance Windows

Planned maintenance reduces unplanned downtime by applying patches, scaling infrastructure, and executing schema migrations during controlled periods. All production maintenance must occur inside an approved **maintenance window** unless emergency change procedures apply.

**Standard maintenance window schedule:**

- Primary window: Sundays 02:00–06:00 UTC in each region's local equivalent mapping.
- Secondary window: Wednesdays 03:00–05:00 UTC for low-risk configuration changes only.

Customers receive notification at least seventy-two hours before standard maintenance. Maintenance that may cause visible interruption includes expected duration, affected endpoints, and rollback plan summary.

**Maintenance window rules:**

- No more than two customer-visible maintenance events per region per calendar month unless approved by platform leadership.
- Database migrations with lock risk require dry-run validation in staging and automated rollback scripts.
- Emergency maintenance outside the **maintenance window** requires platform director approval and same-day customer communication.

Maintenance activity is excluded from **platform uptime SLA** downtime calculations when it falls within an announced window and completes within the published duration plus a fifteen-minute grace period.

## Monitoring, Roles, and Review

GroundSeal publishes monthly reliability reports summarizing uptime percentages, incident counts by severity, maintenance events, and error budget status. Synthetic monitoring runs from multiple geographic probe locations at one-minute intervals for core API health checks.

The platform team owns SLA definitions, maintenance scheduling, and reliability reporting. Product management aligns roadmap commitments with error budget policy. Questions about contractual SLA interpretation route to legal and account management.

This overview is reviewed quarterly and updated after material architecture changes or new region launches. Teams must align runbooks and customer-facing status templates within fourteen days of updates.
