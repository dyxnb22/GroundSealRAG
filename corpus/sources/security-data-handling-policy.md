---
source_id: SRC-security-policy
title: Security Data Handling Policy
owner_id: team-security
visibility: confidential
allowed_roles: [admin, security]
sensitivity: critical
freshness_updated_at: "2026-01-10T00:00:00Z"
---

# Security Data Handling Policy

This policy defines how GroundSeal classifies, stores, transmits, and disposes of data across production systems, corporate tools, and employee devices. All personnel with access to confidential systems must comply. Violations may result in access revocation and disciplinary action.

## Purpose and Scope

The Security Data Handling Policy applies to all employees, contractors, and automated services that create, read, update, or delete GroundSeal data. It covers customer records, employee information, financial records, source code, infrastructure credentials, and telemetry. Third-party vendors must meet equivalent requirements under separate agreements.

This document is the authoritative reference for data classification labels, encryption at rest requirements, encryption in transit requirements, retention schedules, and breach notification triggers. Engineering teams must map their services to the classification tiers defined below before storing new data types.

## Data Classification Framework

GroundSeal uses four classification tiers. Every dataset must be labeled at creation time and re-evaluated when its use changes.

**Public** data may be disclosed externally without restriction. Examples include marketing materials and open-source repositories.

**Internal** data is intended for employees and approved contractors with a business need. Examples include internal wiki pages, non-customer product specifications, and aggregated analytics without identifiers.

**Confidential** data requires role-based access and must not leave approved systems without encryption. Examples include customer account details, unreleased product plans tied to identifiable customers, and security incident records.

**Restricted** data carries the highest sensitivity and requires explicit approval for access. Examples include authentication secrets, payment card data, government identifiers, and raw security audit findings.

Classification labels must appear in data catalogs, schema documentation, and ticket descriptions when data is moved or exported.

## Encryption at Rest Requirements

All confidential and restricted data must be encrypted at rest using approved algorithms and key management. GroundSeal mandates AES-256 for block storage and object storage. Database encryption must use platform-managed keys with customer-managed key options for restricted tiers.

**Minimum encryption at rest requirements:**

- Production databases storing confidential or restricted data must enable transparent data encryption with keys rotated at least annually.
- Object storage buckets containing customer uploads must use server-side encryption with a dedicated KMS key per environment.
- Laptop full-disk encryption is mandatory for any device that may cache confidential data, including developer machines with production read replicas.
- Backup snapshots inherit the classification of source data and must remain encrypted; unencrypted backup exports are prohibited.
- Secrets must never be stored in plaintext on disk; use the approved secrets manager with automatic rotation hooks.

Key custody follows the principle of separation of duties. Security operations holds break-glass procedures; application teams request key usage through audited IAM roles. Any exception to encryption at rest requirements requires a written risk acceptance signed by the CISO.

## Encryption in Transit Requirements

Data in motion must be protected against interception and tampering. GroundSeal requires TLS 1.2 or higher for all external and internal service-to-service communication. Self-signed certificates are not permitted in production paths.

**Minimum encryption in transit requirements:**

- All public HTTP endpoints must redirect to HTTPS and enforce HSTS with a minimum max-age of one year.
- Internal gRPC and REST calls between services must use mTLS where the service mesh is deployed.
- Email containing confidential attachments must use approved secure delivery mechanisms; standard SMTP without encryption is insufficient.
- VPN or zero-trust client requirements apply when accessing administrative consoles from non-corporate networks.
- File transfers to vendors must use SFTP, signed HTTPS uploads, or equivalent approved channels.

Certificate management is centralized. Teams must not deploy long-lived certificates beyond ninety days without automation. Misconfigured TLS endpoints are treated as severity-high findings in vulnerability scans.

## Data Retention and Disposal

Retention periods align with legal, contractual, and operational needs. Customer data is retained for the life of the contract plus the statutory period defined in the Data Processing Addendum. Employee records follow HR retention schedules. Security logs are retained for thirteen months unless a longer hold applies to an active investigation.

Disposal requires cryptographic erasure or physical destruction for restricted media. Soft deletes in application databases are not sufficient for regulated deletion requests; run approved purge jobs and verify completion in audit logs.

## Access Control and Least Privilege

Access to confidential and restricted data is granted through role assignments tied to job function. Standing broad admin access is discouraged. Just-in-time elevation with ticket approval is required for production database writes and secrets manager admin roles.

Quarterly access reviews validate that each grant remains justified. Orphaned accounts and excess permissions are remediated within five business days of review completion.

## Logging, Monitoring, and Audit

Systems handling confidential data must emit structured audit events for authentication, authorization decisions, data exports, and configuration changes. Logs must not contain restricted secrets or full payment card numbers. Security operations monitors for anomalous download volume, off-hours bulk exports, and failed decryption attempts.

## Incident and Breach Handling

Suspected unauthorized access to classified data must be reported immediately through the incident response channel. Do not delete evidence or notify external parties before the security team assesses scope. This policy links to the Incident Response Runbook for escalation paths.

## Compliance and Training

All personnel complete annual data handling training. Teams onboarding new services must complete a data inventory worksheet and obtain security sign-off before production launch. Internal audits sample encryption configurations, classification accuracy, and access reviews each quarter.

## Policy Maintenance

The security team owns this policy. Material changes require review by legal and engineering leadership. The current version supersedes all prior drafts. Questions should be routed to `#team-security` or the security helpdesk queue.
