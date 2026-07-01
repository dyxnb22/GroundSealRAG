---
source_id: SRC-data-retention
title: Data Retention Policy
owner_id: team-compliance
visibility: internal
allowed_roles: [admin, legal, engineer]
sensitivity: medium
freshness_updated_at: "2026-02-10T00:00:00Z"
---

# Data Retention Policy

This policy defines how long GroundSeal retains operational, customer, and compliance-related data across production systems, backups, and observability stores. It applies to all teams that create, store, or delete records on behalf of GroundSeal or its customers. Engineering, legal, and compliance stakeholders share responsibility for enforcing these schedules and documenting exceptions.

## Purpose and Scope

The Data Retention Policy establishes retention periods aligned with contractual obligations, regulatory requirements, and operational needs. It covers customer account data, application telemetry, audit logs, support tickets, financial records, and infrastructure backups. Active legal holds supersede standard schedules until compliance releases them.

Teams must map each dataset to a retention class before production deployment. New data types require compliance review when no existing class applies. Retention decisions must be recorded in the data catalog with owner, classification, and purge mechanism.

## Data Retention Period by Category

GroundSeal assigns a **data retention period** to every managed dataset. The retention period begins at creation or last meaningful update, depending on category rules below.

**Customer account and configuration data** is retained for the duration of the active subscription plus ninety days after contract termination unless the Data Processing Addendum requires longer. During the post-termination window, data remains available for export and then enters scheduled purge.

**Transactional and usage records** supporting billing and metering are retained for seven years. Aggregated analytics with identifiers removed may be retained indefinitely in internal-only stores.

**Employee records** follow HR schedules: active employment plus seven years for personnel files and three years for routine correspondence.

**Security and compliance artifacts**, including penetration test reports, are retained for five years. Legal agreements are retained for the life of the relationship plus ten years.

**Ephemeral caches and session tokens** must expire within twenty-four hours. Temporary processing queues should auto-delete completed jobs within seventy-two hours.

Any extension beyond standard **data retention period** limits requires written approval from compliance and legal with a defined review date.

## Backup Retention

Backups protect against data loss and support disaster recovery. Backup retention must not exceed the retention period of the source data classification unless encrypted and access-restricted under break-glass procedures.

**Production database snapshots** follow tiered schedules:

- Continuous point-in-time recovery windows are maintained for thirty-five days in primary regions.
- Daily full snapshots are retained according to **backup retention 90 days** for standard production databases.
- Weekly snapshots for long-term recovery are retained for one year before automatic expiration.

**Object storage backups** for customer uploads mirror source bucket lifecycle rules. When source objects are deleted under a valid **customer data deletion request**, corresponding backup copies must be purged within the next backup compaction cycle, not to exceed thirty days.

Backup access is limited to platform operations and disaster recovery roles. Restoration events require ticket approval and are logged in the audit trail.

## Customer Data Deletion

GroundSeal honors contractual and regulatory obligations to delete customer data upon request or at contract end. A **customer data deletion request** initiates a tracked workflow in the privacy operations queue.

Requests may arrive via the admin console, signed email from an authorized account administrator, or legal channel. Support validates requester authority before assignment. Legal reviews requests involving active disputes or subpoenas.

**Execution requirements:**

- Application databases: run approved purge jobs that remove tenant-scoped rows and invalidate related cache keys.
- Search indexes and vector stores: delete embeddings and metadata keyed to the tenant identifier.
- Backups: mark tenant scope for exclusion during the next compaction window per backup retention rules.
- Third-party subprocessors: confirm deletion or return certificates of destruction within contractual timelines.

Engineering attaches purge job identifiers to the ticket. Compliance samples deleted tenants to confirm absence from query surfaces accessible to other customers. Customers receive written confirmation when deletion is complete.

Soft deletes alone do not satisfy a **customer data deletion request**. Hard purge with audit evidence is mandatory unless an explicit legal hold prevents deletion.

## Log Retention Schedule

Observability and audit logs support security monitoring, incident investigation, and compliance evidence. Log retention balances investigative value against storage cost and privacy minimization.

| Log type | Retention | Notes |
|----------|-----------|-------|
| Authentication and authorization audit | 13 months | Includes failed login and privilege elevation |
| Application request logs (production) | 90 days | Full payloads excluded for confidential fields |
| Security information and event management | 13 months | Extended hold during active investigations |
| Infrastructure and container logs | 30 days | Extended to 90 days for payment-adjacent services |
| Change management and deployment audit | 3 years | Immutable store with hash verification |
| Customer support interaction logs | 3 years | Redact payment details at ingestion |

Security operations may apply temporary extended retention to log subsets tied to an open incident. Log pipelines must strip restricted secrets and payment card numbers at collection time.

## Roles and Review

Compliance owns this policy and conducts annual reviews. Engineering implements purge automation and monitors job failures. Legal approves exceptions and manages holds. Exceptions require a risk assessment, compensating controls, and expiration date.

This policy is reviewed at least annually and after material regulatory or product changes. Updates are communicated through the internal policy portal. Teams must reconcile service documentation within thirty days of publication.
