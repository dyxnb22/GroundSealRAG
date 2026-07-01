from __future__ import annotations

from dataclasses import dataclass, field

from groundseal.citations.packer import CitationPacker
from groundseal.freshness.filter import FreshnessFilter
from groundseal.models.candidate import CandidateRecord
from groundseal.models.chunk import ChunkRecord
from groundseal.models.citation import CitationPackage
from groundseal.models.permission import PermissionDecision
from groundseal.permissions.filter import PermissionFilter
from groundseal.permissions.requester import RequesterContext
from groundseal.retrieval.hybrid import HybridRetriever
from groundseal.retrieval.lexical import LexicalRetriever
from groundseal.retrieval.rerank import CrossEncoderReranker
from groundseal.retrieval.semantic import SemanticRetriever

VALID_METHODS = frozenset({"lexical", "semantic", "hybrid"})


@dataclass
class RetrievalResult:
    query: str
    requester_id: str
    method: str
    candidates: list[CandidateRecord] = field(default_factory=list)
    allowed_candidates: list[CandidateRecord] = field(default_factory=list)
    denied_candidates: list[CandidateRecord] = field(default_factory=list)
    permission_decisions: list[PermissionDecision] = field(default_factory=list)
    citation_package: CitationPackage | None = None
    stale_excluded: int = 0


class RetrievalPipeline:
    def __init__(
        self,
        chunks: list[ChunkRecord],
        lexical: LexicalRetriever,
        semantic: SemanticRetriever,
        hybrid: HybridRetriever,
        permission_filter: PermissionFilter | None = None,
        citation_packer: CitationPacker | None = None,
        freshness_filter: FreshnessFilter | None = None,
        reranker: CrossEncoderReranker | None = None,
    ) -> None:
        self.chunks = chunks
        self.chunk_map = {c.chunk_id: c for c in chunks}
        self.lexical = lexical
        self.semantic = semantic
        self.hybrid = hybrid
        self.permission_filter = permission_filter or PermissionFilter()
        self.citation_packer = citation_packer or CitationPacker()
        self.freshness_filter = freshness_filter
        self.reranker = reranker

    def _search(self, query: str, method: str, top_k: int) -> list[CandidateRecord]:
        if method == "lexical":
            return self.lexical.search(query, top_k=top_k)
        if method == "semantic":
            return self.semantic.search(query, top_k=top_k)
        if method == "hybrid":
            return self.hybrid.search(query, top_k=top_k)
        raise ValueError(f"Unknown retrieval method: {method}. Choose from {sorted(VALID_METHODS)}")

    def retrieve(
        self,
        query: str,
        requester: RequesterContext,
        method: str = "hybrid",
        top_k: int = 10,
        pack: bool = False,
        rerank: bool = False,
        exclude_stale: bool = False,
    ) -> RetrievalResult:
        if method not in VALID_METHODS:
            raise ValueError(f"Unknown retrieval method: {method}. Choose from {sorted(VALID_METHODS)}")

        candidates = self._search(query, method, top_k)
        stale_excluded = 0

        if exclude_stale and self.freshness_filter:
            fresh_candidates = []
            for cand in candidates:
                if self.freshness_filter.is_stale(cand.source_id):
                    stale_excluded += 1
                else:
                    fresh_candidates.append(cand)
            candidates = fresh_candidates

        allowed, decisions, denied = self.permission_filter.filter_candidates(
            candidates, self.chunk_map, requester
        )

        if rerank:
            if self.reranker is None:
                self.reranker = CrossEncoderReranker()
            if allowed:
                allowed = self.reranker.rerank(query, allowed, self.chunk_map)

        result = RetrievalResult(
            query=query,
            requester_id=requester.requester_id,
            method=method,
            candidates=candidates,
            allowed_candidates=allowed,
            denied_candidates=denied,
            permission_decisions=decisions,
            stale_excluded=stale_excluded,
        )

        if pack:
            perm_map = {d.chunk_id: d.decision for d in decisions}
            result.citation_package = self.citation_packer.pack(
                query, requester.requester_id, allowed, self.chunk_map, perm_map
            )

        return result
