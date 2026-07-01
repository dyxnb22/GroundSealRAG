---
source_id: SRC-support-playbook
title: Customer Support Playbook
owner_id: team-support
visibility: internal
allowed_roles: [support, admin]
sensitivity: medium
freshness_updated_at: "2026-02-20T00:00:00Z"
---

# Customer Support Playbook

This playbook guides GroundSeal customer support agents through ticket handling, triage, escalation, and communication standards. It applies to email, chat, and phone channels. Agents should follow these procedures to deliver consistent, secure, and auditable customer experiences.

## Support Mission and Scope

Support helps customers resolve product issues, answer authorized questions about features, and route defects or security concerns to engineering. Support does not provide legal advice, modify customer contracts, or bypass permission controls in retrieval products.

Agents represent GroundSeal in every interaction. Professional tone, accurate information, and timely follow-up are mandatory.

## Ticket Intake Channels

Tickets arrive through the CRM from email, in-app chat, community escalations, and executive forwards. Each channel creates a unified ticket record with customer identity, product tier, and SLA clock.

Verify customer identity before discussing account-specific details. Use approved authentication challenges; do not accept unverified third-party requests for data export or access changes.

## Ticket Triage

Ticket triage sorts new work by urgency, impact, and topic so the right queue receives it quickly. Triage occurs within fifteen minutes for premium tiers and sixty minutes for standard tiers during business hours.

**Ticket triage steps:**

1. Confirm duplicate tickets and merge when the same incident is reported multiple times.
2. Classify product area: ingestion, retrieval, permissions, citations, billing, or account administration.
3. Assign priority using the matrix below aligned with customer SLA tier.
4. Apply tags for known incidents or feature gaps linked to internal tracking tickets.
5. Route to tier-appropriate queue: general, technical, or billing.
6. Send initial acknowledgment with ticket ID and expected next update time.

Misclassified tickets delay resolution; when uncertain, escalate to the technical queue with notes rather than bouncing between agents.

## Priority Matrix

**Urgent:** Production outage, data loss risk, or security suspicion affecting customer operations. Response within one hour; updates every two hours until mitigated.

**High:** Major feature impairment with workaround unavailable. Response within four hours.

**Normal:** Functional questions, non-blocking bugs, configuration assistance. Response within one business day.

**Low:** Feature requests, documentation feedback, cosmetic issues. Response within three business days.

Security-related reports bypass standard marketing of self-service articles until validated.

## First Response Standards

First responses acknowledge the issue, restate the customer goal, and outline next steps. Avoid promising fixes without engineering confirmation. Link only to public or customer-authorized documentation.

Templates exist for common scenarios but must be personalized. Never paste internal runbook excerpts containing confidential identifiers.

## Troubleshooting Workflow

Technical tickets follow structured diagnosis:

- Gather environment details: deployment region, integration type, corpus size, and recent changes.
- Reproduce when possible in staging with customer permission and sanitized data.
- Check status page and internal incident channels for correlated events.
- Document hypotheses and eliminated causes in ticket notes for shift handoffs.
- Propose workaround while permanent fix is developed when available.

Permission-related tickets require verifying requester roles in customer identity systems before suggesting configuration changes.

## Escalation Procedures

Escalation moves tickets to specialized teams when frontline agents exceed authority, expertise, or time thresholds.

**When to escalate:**

- Suspected security incident or data exposure — escalate immediately to security on-call and mark ticket sensitive.
- Confirmed product defect requiring engineering fix — create linked engineering ticket and notify customer of tracking ID.
- Billing disputes over five thousand dollars — escalate to finance operations manager.
- Legal, export control, or regulatory requests — escalate to legal queue; do not commit to compliance outcomes.
- Customer executive escalation or churn risk flagged by account management — notify customer success director within two hours.

Escalation handoffs include complete timeline, customer impact summary, and explicit ask of the receiving team. Do not re-open resolved tickets without new information.

## Customer Communication During Incidents

During company-wide incidents, use approved status messaging only. Support aligns customer communications with incident command updates. Do not speculate about root cause or name internal personnel.

Post-incident, offer follow-up to affected customers with summary of impact and remediation when communications lead approves external detail.

## Data Handling in Support Tools

Redact secrets, tokens, and personal data unnecessary for resolution before attaching logs to tickets. Follow retention schedules; close tickets trigger archival according to CRM policy.

Agents must not store customer exports on personal devices.

## Quality and Coaching

Team leads sample tickets weekly for tone, accuracy, and procedure adherence. Coaching focuses on triage speed, escalation judgment, and documentation quality.

Customer satisfaction surveys feed monthly reviews. Repeated low scores trigger paired sessions and updated macros where gaps are systemic.

## Shift Handoffs

Outgoing agents leave notes on open urgent and high tickets with current status and promised follow-ups. Handoff meetings occur at shift boundaries in shared regions.

## Knowledge Base and Self-Service

Before escalating internally, search the internal knowledge base for verified articles matching the customer symptom. Link customers to public documentation when it fully answers the question. If documentation is wrong or missing, file a documentation defect ticket so product education stays aligned with retrieval behavior changes.

## Playbook Maintenance

Support operations owns this playbook. Product changes triggering new triage categories require playbook updates before launch. Suggestions go to `#team-support-leads`. Quarterly reviews incorporate top ticket themes and failure analysis from the prior quarter so triage tags remain accurate.
