from __future__ import annotations

from groundseal.models.chunk import ChunkRecord
from groundseal.models.permission import PermissionDecision
from groundseal.models.source import utc_now_iso
from groundseal.permissions.requester import RequesterContext

VISIBILITY_ORDER = ["public", "general", "internal", "hr-only", "confidential", "legal"]
ADMIN_ROLES = {"admin"}


def _visibility_allowed(requester: RequesterContext, visibility: str) -> bool:
    if not requester.allowed_visibilities:
        return False
    if visibility not in VISIBILITY_ORDER:
        return False
    max_allowed = max(
        (VISIBILITY_ORDER.index(v) for v in requester.allowed_visibilities if v in VISIBILITY_ORDER),
        default=-1,
    )
    vis_idx = VISIBILITY_ORDER.index(visibility)
    return vis_idx <= max_allowed


class PermissionFilter:
    def evaluate_chunk(self, chunk: ChunkRecord, requester: RequesterContext) -> PermissionDecision:
        # deny-by-default on missing metadata
        if not chunk.visibility or not chunk.allowed_roles:
            return PermissionDecision(
                chunk_id=chunk.chunk_id,
                requester_id=requester.requester_id,
                decision="deny",
                reason_code="missing_metadata",
                matched_rule="deny_by_default",
                evaluated_at=utc_now_iso(),
            )

        if requester.allowed_source_ids is not None:
            if chunk.source_id not in requester.allowed_source_ids:
                return PermissionDecision(
                    chunk_id=chunk.chunk_id,
                    requester_id=requester.requester_id,
                    decision="deny",
                    reason_code="source_not_allowed",
                    matched_rule="explicit_source_list",
                    evaluated_at=utc_now_iso(),
                )
            if _visibility_allowed(requester, chunk.visibility):
                return PermissionDecision(
                    chunk_id=chunk.chunk_id,
                    requester_id=requester.requester_id,
                    decision="allow",
                    reason_code="explicit_source_grant",
                    matched_rule="allowed_source_ids",
                    evaluated_at=utc_now_iso(),
                )
            return PermissionDecision(
                chunk_id=chunk.chunk_id,
                requester_id=requester.requester_id,
                decision="deny",
                reason_code="visibility_mismatch",
                matched_rule="explicit_source_list",
                evaluated_at=utc_now_iso(),
            )

        if not requester.roles:
            return PermissionDecision(
                chunk_id=chunk.chunk_id,
                requester_id=requester.requester_id,
                decision="deny",
                reason_code="no_roles",
                matched_rule="deny_by_default",
                evaluated_at=utc_now_iso(),
            )

        if ADMIN_ROLES.intersection(requester.roles):
            if _visibility_allowed(requester, chunk.visibility):
                return PermissionDecision(
                    chunk_id=chunk.chunk_id,
                    requester_id=requester.requester_id,
                    decision="allow",
                    reason_code="admin_role",
                    matched_rule="role_admin",
                    evaluated_at=utc_now_iso(),
                )

        role_match = bool(set(requester.roles) & set(chunk.allowed_roles))
        vis_ok = _visibility_allowed(requester, chunk.visibility)

        if role_match and vis_ok:
            return PermissionDecision(
                chunk_id=chunk.chunk_id,
                requester_id=requester.requester_id,
                decision="allow",
                reason_code="role_and_visibility",
                matched_rule="role_visibility_match",
                evaluated_at=utc_now_iso(),
            )

        return PermissionDecision(
            chunk_id=chunk.chunk_id,
            requester_id=requester.requester_id,
            decision="deny",
            reason_code="role_or_visibility_mismatch",
            matched_rule="deny_no_match",
            evaluated_at=utc_now_iso(),
        )

    def filter_candidates(
        self,
        candidates: list,
        chunk_map: dict[str, ChunkRecord],
        requester: RequesterContext,
    ) -> tuple[list, list[PermissionDecision], list]:
        allowed = []
        denied = []
        decisions: list[PermissionDecision] = []
        for cand in candidates:
            chunk = chunk_map.get(cand.chunk_id)
            if chunk is None:
                decisions.append(
                    PermissionDecision(
                        chunk_id=cand.chunk_id,
                        requester_id=requester.requester_id,
                        decision="deny",
                        reason_code="chunk_not_found",
                        matched_rule="deny_by_default",
                        evaluated_at=utc_now_iso(),
                    )
                )
                denied.append(cand)
                continue
            decision = self.evaluate_chunk(chunk, requester)
            decisions.append(decision)
            if decision.decision == "allow":
                allowed.append(cand)
            else:
                denied.append(cand)
        return allowed, decisions, denied
