---
source_id: SRC-product-roadmap
title: Quarterly Product Roadmap
owner_id: team-product
visibility: internal
allowed_roles: [engineer, product, admin]
sensitivity: medium
freshness_updated_at: "2026-04-01T00:00:00Z"
---

# Quarterly Product Roadmap

This document outlines GroundSeal product priorities for the current planning cycle. It aligns engineering, design, and go-to-market teams on themes, milestones, and dependencies. Dates are targets, not commitments, and may shift based on customer feedback and capacity.

## Roadmap Principles

We prioritize retrieval quality, permission correctness, and citation fidelity over surface-level feature count. Each milestone includes measurable exit criteria and evaluation cases before general availability. Cross-functional reviews occur at the end of each month.

## Q2 Themes

Q2 focuses on four strategic themes that support enterprise adoption and evaluation readiness.

**Theme 1 — Trustworthy retrieval:** Improve hybrid search accuracy, permission filtering correctness, and evidence assembly for agent workflows. Success means higher recall on seed evaluation cases without unauthorized leakage.

**Theme 2 — Operator visibility:** Give administrators dashboards for source freshness, ingestion health, and failed permission checks. Success means mean time to diagnose retrieval failures drops below two hours.

**Theme 3 — Integration depth:** Ship connectors for common document stores and identity providers used by design partners. Success means two pilot customers ingest production corpora without manual intervention.

**Theme 4 — Citation auditability:** Strengthen citation payloads with stable chunk identifiers, source display names, and permission context for downstream auditors. Success means pilot customers export citation bundles for compliance review.

These Q2 themes guide sprint planning and hiring requests. Features outside the themes require explicit deferral of lower-priority work.

## Milestones

Milestones are numbered M1 through M6 for the quarter. Each milestone lists owner, target week, and dependencies.

**M1 — Corpus ingestion v1 (Week 2):** Complete markdown ingestion with frontmatter permission inheritance and manifest validation. Exit: ten seed documents ingested with stable document IDs.

**M2 — Chunking pipeline (Week 4):** Heading-aware chunking with metadata preservation. Exit: average eight to fifteen chunks per seed document with traceable chunk IDs.

**M3 — Lexical retrieval baseline (Week 6):** BM25 or equivalent over chunk text with permission filter. Exit: pass lexical seed cases at eighty percent top-three source accuracy on full-access requester.

**M4 — Permission enforcement (Week 8):** Deny unauthorized sources in retrieval results and citation output. Exit: zero blocking failures on permission evaluation cases.

**M5 — Hybrid retrieval experiment (Week 10):** Combine lexical and embedding retrieval with failure analysis report. Exit: documented improvement on semantic cases or explicit decision not to adopt.

**M6 — Pilot readiness review (Week 12):** Joint review with design partners covering SLAs, support runbooks, and roadmap for Q3. Exit: signed pilot checklist and open risk register.

Dependencies: M3 requires M2; M4 requires M3; M5 requires M4. Security review gates M4 and M6.

## Customer and Partner Inputs

Design partners requested clearer audit trails for denied retrieval attempts and faster source refresh after policy updates. Sales noted competitive pressure on permission-aware RAG; Q2 themes address those inputs without committing to generation features prematurely.

Support feedback highlighted need for better internal documentation search; a subset of retrieval improvements will dogfood on the support playbook corpus in late Q2.

## Out of Scope for Q2

The following items are explicitly deferred to reduce drift:

- End-user chatbot UI and branded assistant widgets.
- Multi-model routing and automatic answer generation.
- Real-time collaborative editing of source documents.
- Full SOC2 audit package completion, though logging work supports future certification.

Deferrals are revisited during Q2 midpoint planning.

## Metrics and Evaluation

Product reviews track leading indicators weekly: ingestion success rate, evaluation case pass rate, permission denial accuracy, and citation field completeness. Lagging indicators include pilot customer satisfaction scores and support ticket volume related to retrieval.

Failed experiments are recorded in the failure analysis log with hypothesis, setup, and conclusion. Roadmap items do not advance without evaluation evidence.

## Resource and Risk Notes

Engineering capacity assumes stable headcount with one additional platform hire starting mid-quarter. Risk: embedding infrastructure cost overruns if hybrid retrieval scales before caching optimizations land. Mitigation: cap experiment corpus size and batch embedding jobs.

Risk: dependency on identity provider sandbox access for permission testing. Mitigation: maintain synthetic requester fixtures parallel to live directory integration.

## Communication Cadence

Weekly roadmap snippets post to `#product-updates`. Milestone completions trigger brief demo recordings for internal stakeholders. External roadmap summaries exclude confidential partner names and unreleased security details.

## Alignment with Engineering Sprints

Sprint planning maps user stories to milestone IDs so progress rolls up automatically in roadmap dashboards. Carryover work must re-link to an active milestone or move explicitly to the backlog with product approval. This prevents silent slippage of Q2 themes without stakeholder visibility.

## Stakeholder Reviews

Product council meets biweekly to review roadmap health indicators and unblock dependencies between platform, security, and application teams. Decisions to reprioritize milestones require product VP approval and updated exit criteria communicated to engineering managers within one business day.

## Document Maintenance

Product management owns this roadmap. Revisions require changelog notes at the top of the internal wiki mirror. Engineers should treat milestone exit criteria as the definition of done for roadmap-tagged work. Mid-quarter reviews compare actual milestone completion dates against target weeks and document scope adjustments for Q2 themes still in flight.
