# Source Freshness Policy

## Rule

Sources not updated within 90 days are considered stale.

## Behavior

- `FreshnessFilter.is_stale(source_id)` returns true if `freshness_updated_at` > 90 days ago
- Stale chunks may be excluded or downranked by 50%
