---
source_id: SRC-incident-runbook
title: Incident Response Runbook
owner_id: team-security
visibility: confidential
allowed_roles: [admin, security, engineer]
sensitivity: critical
freshness_updated_at: "2026-02-01T00:00:00Z"
---

# Incident Response Runbook

This runbook provides operational procedures for detecting, triaging, escalating, and resolving production and security incidents at GroundSeal. It is intended for on-call engineers, security analysts, and incident commanders. Follow these steps unless a live incident commander explicitly directs otherwise.

## Incident Lifecycle Overview

Every incident progresses through detection, triage, mitigation, recovery, and post-incident review. Incidents are tracked in the central incident management system with a unique identifier, severity level, timeline notes, and linked customer communications. Status updates must be posted at intervals defined by severity.

Do not close an incident until customer impact is verified resolved, monitoring shows stable metrics, and a preliminary root cause category is recorded. Post-incident reviews are mandatory for severity P0 and P1 events.

## Severity Levels

GroundSeal uses four severity levels. Assign severity during initial triage and adjust as facts emerge.

**P0 — Critical:** Complete outage of a customer-facing service, confirmed data breach, or active exploitation with material customer impact. Requires immediate executive notification and all-hands response.

**P1 — High:** Major degradation affecting a significant customer subset, loss of a critical internal system, or credible threat with imminent risk. Requires incident commander within fifteen minutes.

**P2 — Medium:** Partial degradation, non-customer-facing failures with workaround, or security findings requiring same-day remediation.

**P3 — Low:** Minor bugs, isolated alerts with no customer impact, or hygiene tasks discovered during monitoring.

Severity definitions drive paging policy, communication cadence, and post-incident review requirements. When uncertain between two levels, choose the higher severity until disproved.

## P0 Incident Escalation

P0 incident escalation begins the moment a responder confirms customer-visible outage, confirmed unauthorized data access, or equivalent critical impact. Speed and clarity outweigh perfect information.

**P0 incident escalation procedure:**

1. Page the primary on-call engineer and security on-call simultaneously using the P0 bridge.
2. Declare an incident in the management tool with severity P0 and assign an incident commander within five minutes.
3. Open the war room video bridge and post the bridge link in `#incidents` and `#exec-ops`.
4. Notify the VP Engineering and CISO within ten minutes of declaration.
5. Assign roles: incident commander, communications lead, scribe, and technical investigators per affected domain.
6. Begin a public-facing status page update within fifteen minutes if external customers are affected.
7. Escalate to the CEO if customer data exposure is confirmed or outage exceeds sixty minutes.

During P0 incidents, the incident commander has authority to pull any engineer needed for mitigation. Defer non-incident meetings and freeze unrelated production changes unless rollback requires them.

## On-Call Responsibilities

On-call rotation spans platform, product services, and security. Each rotation includes a primary and secondary responder. The primary owns acknowledgment, initial triage, and escalation. The secondary backs up if the primary is unavailable within five minutes.

On-call engineers must have laptop connectivity, access to runbooks, and credentials for production observability tools. Handoffs occur at rotation boundaries with a written summary of open alerts and in-progress changes.

**On-call expectations:**

- Acknowledge pages within five minutes.
- Begin triage within ten minutes of acknowledgment.
- Document all actions in the incident timeline with timestamps.
- Escalate when impact scope exceeds personal expertise or authority.
- Conduct a warm handoff when ending a shift with an active incident.

Schedule swaps require manager approval and calendar updates to the paging system.

## Detection and Initial Triage

Incidents arrive via automated alerts, customer support tickets, internal reports, or threat intelligence. The first responder validates signal versus noise, identifies affected services, and estimates blast radius.

Triage checklist:

- Confirm alert fidelity using dashboards and recent deploys.
- Identify start time and whether impact is ongoing.
- Check for concurrent changes such as deployments, feature flags, or infrastructure edits.
- Determine customer segments affected and data sensitivity involved.
- Assign preliminary severity and open an incident record.

If triage suggests security compromise, loop in security on-call before attempting broad remediation that could destroy evidence.

## Communication Standards

Internal updates use `#incidents` with structured messages: status, impact, next step, and ETA for the next update. Customer-facing communications are drafted by the communications lead and approved by the incident commander.

P0 updates occur every fifteen minutes until mitigation stabilizes. P1 updates occur every thirty minutes. Avoid speculative root cause in external messages; state observed impact and remediation progress.

## Mitigation and Recovery

Mitigation prioritizes stopping customer harm: rollback, traffic shedding, feature disablement, or isolation of compromised components. Document each action before and after execution. Prefer reversible changes when time permits.

Recovery validates service level objectives, runs smoke tests, and monitors error budgets for at least thirty minutes before declaring resolution. Security incidents may require credential rotation, forensic imaging, and legal hold before full recovery.

## Post-Incident Review

Within five business days of a P0 or P1 closure, conduct a blameless post-incident review. Produce a written report with timeline, root cause, contributing factors, action items, and owners. Track action items to completion in the engineering backlog.

## Runbook Maintenance

The security and platform teams co-own this runbook. After each major incident, update procedures that failed in practice. Drill P0 incident escalation quarterly through tabletop exercises.
