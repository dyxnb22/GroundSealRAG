# Generation Contract

## Constraints

1. Generator consumes `CitationPackage` only — no independent retrieval.
2. Every claim must map to a `citation_id`.
3. Insufficient evidence → explicit refusal message.
4. No conversational multi-turn behavior.

## Output

```json
{
  "answer": "...",
  "claims": [{"text": "...", "citation_id": "..."}],
  "citations_used": ["CITE-..."],
  "status": "grounded | insufficient_evidence"
}
```
