# Permission Test Matrix

| Case | Requester | Query intent | Expected |
|------|-----------|--------------|----------|
| PERM-01 | engineer_std | confidential security policy | deny relevant evidence |
| PERM-02 | contractor_limited | remote work | allow SRC-remote-work only |
| PERM-03 | admin_full | any internal | allow |
| PERM-04 | guest_none | any | deny all |
| PERM-05 | hr_manager | expense policy | allow hr-only |
| PERM-06 | engineer_std | onboarding guide | deny hr-only |

**Blocking metric**: `unauthorized_in_top_k` must be 0.
