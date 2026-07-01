---
source_id: SRC-api-auth
title: API Authentication Specification
owner_id: team-platform
visibility: internal
allowed_roles: [engineer, admin, security]
sensitivity: medium
freshness_updated_at: "2026-01-15T00:00:00Z"
---

# API Authentication Specification

This specification describes how clients authenticate to GroundSeal HTTP APIs. It covers bearer tokens, OAuth2 flows, service credentials, and operational rotation requirements. Implementations must conform before production exposure of new endpoints.

## Authentication Model Overview

GroundSeal APIs use a layered authentication model. Human-initiated integrations typically use OAuth2 authorization code flow with PKCE. Machine-to-machine integrations use client credentials or scoped service tokens. Legacy integrations may use long-lived API keys only when approved by platform security.

Every request must include credentials in the `Authorization` header unless explicitly documented otherwise. Anonymous access is limited to health checks and public metadata endpoints.

## Bearer Tokens

Bearer tokens are opaque or JWT credentials presented as `Authorization: Bearer <token>`. The API gateway validates signature, expiration, audience, and scopes before routing to upstream services.

**Bearer token rules:**

- Tokens must be transmitted only over TLS 1.2 or higher.
- Clients must not embed bearer tokens in URLs, query strings, or client-side logs.
- Short-lived access tokens should be paired with refresh tokens where user sessions apply.
- Services must reject tokens missing required scope claims for the requested operation.
- Token introspection endpoints are available for internal debugging; production traffic should rely on local JWT validation with cached keys.

When a bearer token is compromised, revoke it immediately through the admin console or revocation API and initiate the API token rotation procedure for affected integrations.

## OAuth2 Flows

GroundSeal supports OAuth2 as defined in RFC 6749 with extensions for PKCE on public clients.

**Authorization code with PKCE:** Used by web and mobile applications acting on behalf of users. Clients register redirect URIs in the developer portal. The authorization server issues authorization codes exchanged for access and refresh tokens at the token endpoint.

**Client credentials:** Used by backend services without user context. Clients authenticate with a client ID and secret or mTLS certificate. Issued tokens carry service identity and fine-grained scopes.

**Refresh token rotation:** Refresh tokens are single-use where supported. Reuse detection triggers revocation of the token family.

Token endpoints return standard error codes. Clients must implement exponential backoff on `429` and `503` responses.

## API Token Rotation Procedure

Long-lived API tokens and service credentials require scheduled rotation to limit exposure window. Platform security mandates rotation at least every ninety days for production integrations, or immediately upon personnel change, suspected leak, or vendor offboarding.

**API token rotation procedure:**

1. Create a new token or client secret in the developer portal without deleting the existing credential.
2. Update staging environments first; run automated contract tests against authenticated endpoints.
3. Deploy configuration changes to production using the dual-credential window; both old and new tokens remain valid for up to seventy-two hours.
4. Monitor authentication error rates and success metrics during the overlap period.
5. Revoke the previous token only after confirming zero production traffic uses the old credential for twenty-four consecutive hours.
6. Record rotation completion in the change log with ticket reference and operator identity.
7. For OAuth2 client secrets, update all deployment secrets stores and restart affected workers to pick up new values.

Emergency rotation skips the overlap window when compromise is confirmed. Follow the incident runbook and notify dependent teams through `#platform-alerts`.

## Scope and Authorization

Scopes encode permitted actions as colon-separated strings, for example `documents:read` or `admin:users:write`. Endpoints document required scopes in OpenAPI specifications. Authorization middleware enforces scope checks after authentication succeeds.

Admin scopes require additional step-up authentication or break-glass approval depending on environment.

## Identity When Calling HTTP APIs

Clients prove identity by presenting valid credentials tied to a registered application or user. Human callers using OAuth2 establish identity through the authorization server login and consent. Service callers establish identity through client credentials mapped to a service principal record.

The `sub` claim in JWT access tokens identifies the subject. Service tokens include a `client_id` claim. Downstream services must propagate identity context using signed internal headers rather than re-trusting external tokens inside the mesh.

## Error Handling and Observability

Authentication failures return `401 Unauthorized` with a `WWW-Authenticate` header where applicable. Authorization failures return `403 Forbidden`. Clients must not retry indefinitely on `401` without refreshing credentials.

Authentication events are logged with request ID, client ID, outcome, and failure reason code. Logs exclude raw tokens and secrets.

## Developer Portal and Credential Storage

Applications register in the developer portal to obtain client IDs, configure redirect URIs, and manage tokens. Secrets displayed once at creation must be stored in the approved secrets manager, not in source control.

CI pipelines retrieve short-lived tokens via OIDC federation where available instead of static secrets.

## Compliance and Review

New authentication patterns require architecture review. Deprecated patterns such as basic authentication over user passwords are not permitted for new integrations. Quarterly audits sample active tokens for age, scope appropriateness, and owner validity.

## Specification Maintenance

The platform team owns this document. Breaking changes publish with a ninety-day deprecation notice unless security requires immediate action. Questions belong in `#team-platform` or the API office hours calendar.
