---
source_id: SRC-vendor-access
title: Vendor Access Agreement Summary
owner_id: team-legal
visibility: legal
allowed_roles: [admin, legal]
sensitivity: high
freshness_updated_at: "2026-01-25T00:00:00Z"
---

# Vendor Access Agreement Summary

This summary describes standard terms GroundSeal requires before vendors receive access to facilities, systems, or confidential information. It is a reference for legal, procurement, and security teams negotiating third-party relationships. The full Master Services Agreement and Data Processing Addendum supersede this summary when executed.

## Purpose

Vendor relationships introduce supply chain risk. Standardized access terms ensure vendors protect GroundSeal data, limit scope, and remain accountable for subprocessors and personnel. No vendor receives production access without signed agreements and completed security review.

## Vendor NDA Requirements

All vendors with potential access to non-public information must execute a mutual or one-way non-disclosure agreement before receiving technical documentation, customer data, or system credentials.

**Vendor NDA minimum terms:**

- Definition of confidential information includes business plans, customer lists, security architecture, source code, and aggregated usage metrics not publicly released.
- Obligation to use confidential information only for the stated engagement purpose.
- Prohibition on disclosure to subprocessors without GroundSeal written consent and equivalent binding obligations.
- Return or destruction of confidential materials upon termination within thirty days with written certification.
- Survival of confidentiality obligations for five years after termination, or longer for trade secrets.
- Injunctive relief acknowledgment for unauthorized disclosure.
- Governing law and venue consistent with GroundSeal corporate jurisdiction unless regional entity requires local variation.

Pilot engagements without MSA still require NDA execution. Oral NDAs are not accepted.

## Access Scope Definition

Access scope must be documented in the vendor access schedule attached to each agreement. Vague blanket access is prohibited.

**Access scope elements:**

- Named systems, environments (staging only versus production), and interfaces permitted.
- Authentication method: individual accounts, no shared credentials; MFA mandatory for remote access.
- Data categories permitted including classification labels from the security data handling policy.
- Personnel list with role justification; updates require approval before new individuals receive access.
- Time bounds: project end date, automatic expiry, and renewal approval path.
- Permitted operations: read-only versus read-write; administrative privileges require CISO approval.
- Logging and audit requirements including GroundSeal right to review vendor access logs on request.

Access scope narrower than business ask is preferred; expand only with documented need and compensating controls.

## Security and Compliance Obligations

Vendors must meet baseline security controls proportional to access level.

- SOC2 Type II report or equivalent within twelve months for vendors processing confidential data.
- Incident notification within twenty-four hours of confirmed unauthorized access involving GroundSeal data.
- Vulnerability remediation SLAs for critical findings affecting shared integrations.
- Background checks for personnel with production access where legally permitted.
- Secure development practices if vendor ships code deployed in GroundSeal environments.

Exceptions require risk acceptance signed by legal and security leadership with expiration date.

## Subprocessors and Fourth Parties

Vendors using subprocessors must disclose them before processing begins and notify changes thirty days in advance. GroundSeal maintains a subprocessor approval list. Unauthorized subprocessors constitute material breach.

## Physical and Logical Access Provisioning

Physical office access requires badge issuance logs and escort rules for non-employee vendors in restricted areas. Logical access provisioning follows the joiner-mover-leaver ticket workflow with legal and security approval recorded.

Vendor accounts use distinct naming conventions and are disabled within twenty-four hours of contract end or personnel removal.

## Monitoring and Audit Rights

GroundSeal reserves the right to audit vendor compliance with access terms annually or upon reasonable suspicion of breach. Vendors cooperate with questionnaires, evidence collection, and on-site reviews with reasonable notice.

## Termination and Offboarding

Upon engagement end, vendors must:

- Revoke credentials and VPN access immediately on termination effective time.
- Return devices and destroy copies of GroundSeal data per NDA certification.
- Confirm subprocessor data deletion where applicable.

Legal verifies completion before closing vendor record. Security scans for dormant vendor integrations quarterly.

## Liability and Indemnification

Standard agreements include indemnification for data breaches caused by vendor negligence, IP infringement in deliverables, and violation of applicable privacy laws. Liability caps vary by contract tier; legal must approve uncapped liability only for strategic vendors with board visibility.

## Standard versus Non-Standard Terms

Procurement uses the standard vendor access schedule template. Deviations require legal review checklist completion. Common negotiated points include insurance limits, audit frequency, and subprocessors in regulated industries.

## Roles and Responsibilities

Legal owns contract language. Security owns technical control verification. Procurement owns commercial terms and vendor master data. Business sponsors own business justification for access scope requests.

## Related Documents

Full templates reside in the legal document repository. Cross-reference the Security Data Handling Policy for classification and encryption requirements vendors must mirror.

## Insurance and Financial Assurance

Standard vendor agreements require general liability and cyber liability insurance at minimum limits published in the procurement handbook. Vendors processing restricted data may need higher limits or proof of financial stability before production access scope is granted.

## Summary Maintenance

Legal operations updates this summary when standard terms change. Version history tracks effective dates. Distribution limited to admin and legal roles per visibility classification. Procurement receives change notices when vendor NDA or access scope templates are revised.
