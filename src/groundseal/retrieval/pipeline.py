from __future__ import annotations

from dataclasses import dataclass, field

from groundseal.chunking.baseline import BaselineChunker
from groundseal.citations.packer import CitationPacker
from groundseal.models.candidate import CandidateRecord
from groundseal.models.chunk import ChunkRecord
from groundseal.models.citation import CitationPackage
from groundseal.models.permission import PermissionDecision
from groundseal.permissions.filter import PermissionFilter
from groundseal.permissions.requester import RequesterContext
from groundseal.retrieval.hybrid import HybridRetriever
from groundseal.retrieval.lexical import LexicalRetriever
from groundseal.retrieval.semantic import SemanticRetriever


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


class RetrievalPipeline:
    def __init__(
        self,
        chunks: list[ChunkRecord],
        lexical: LexicalRetriever,
        semantic: SemanticRetriever,
        hybrid: HybridRetriever,
        permission_filter: PermissionFilter | None = None,
        citation_packer: CitationPacker | None = None,
        reranker=None,
    ) -> None:
        self.chunks = chunks
        self.chunk_map = {c.chunk_id: c for c in chunks}
        self.lexical = lexical
        self.semantic = semantic
        self.hybrid = hybrid
        self.permission_filter = permission_filter or PermissionFilter()
        self.citation_packer = citation_packer or CitationPacker()
        self.reranker = reranker

    def retrieve(
        self,
        query: str,
        requester: RequesterContext,
        method: str = "hybrid",
        top_k: int = 10,
        pack: bool = False,
        rerank: bool = False,
    ) -> RetrievalResult:
        if method == "lexical":
            candidates = self.lexical.search(query, top_k=top_k)
        elif method == "semantic":
            candidates = self.semantic.search(query, top_k=top_k)
        else:
            candidates = self.hybrid.search(query, top_k=top_k)

        allowed, decisions, denied = self.permission_filter.filter_candidates(
            candidates, self.chunk_map, requester
        )

        if rerank and self.reranker and allowed:
            allowed = self.reranker.rerank(query, allowed, self.chunk_map)

        result = RetrievalResult(
            query=query,
            requester_id=requester.requester_id,
            method=method,
            candidates=candidates,
            allowed_candidates=allowed,
            denied_candidates=denied,
            permission_decisions=decisions,
        )

        if pack:
            perm_map = {d.chunk_id: d.decision for d in decisions}
            result.citation_package = self.citation_packer.pack(
                query, requester.requester_id, allowed, self.chunk_map, perm_map
            )

        return result
