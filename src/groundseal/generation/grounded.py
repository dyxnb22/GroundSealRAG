from __future__ import annotations

from groundseal.models.citation import CitationPackage


class GroundedGenerator:
    """Template-based grounded answer from CitationPackage — not a chatbot."""

    def generate(self, package: CitationPackage) -> dict:
        if not package.citations:
            return {
                "answer": "Insufficient evidence to answer this query.",
                "claims": [],
                "citations_used": [],
                "status": "insufficient_evidence",
            }

        claims = []
        cite_ids = []
        for cite in package.citations:
            claim_text = f"Based on [{cite.label}]: {cite.excerpt[:200].strip()}"
            claims.append({"text": claim_text, "citation_id": cite.citation_id})
            cite_ids.append(cite.citation_id)

        answer = " ".join(c["text"] for c in claims[:3])
        return {
            "answer": answer,
            "claims": claims,
            "citations_used": cite_ids,
            "status": "grounded",
        }
