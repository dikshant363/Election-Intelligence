"""Hybrid Retrieval engine combining lexical FTS search with semantic vector search via RRF."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.embeddings import EmbeddingProvider, MockEmbeddingProvider
from app.ai.vector import VectorStore
from app.search.queries import SearchQuery
from app.search.services import SearchService

RRF_CONSTANT = 60.0


@dataclass
class RetrievedDocument:
    """Standardized document returned from hybrid retrieval."""

    id: str
    entity_type: str
    title: str
    content: str
    score: float
    retrieval_mode: str = "hybrid"
    metadata: dict[str, Any] = field(default_factory=dict)


class HybridRetriever:
    """
    Hybrid retrieval coordinator.
    Combines lexical search (from SearchService SAL) and semantic vector search using Reciprocal Rank Fusion (RRF).
    """

    def __init__(
        self,
        session: AsyncSession,
        embedding_provider: EmbeddingProvider | None = None,
        vector_store: VectorStore | None = None,
    ) -> None:
        self._search_service = SearchService(session)
        self._embedding_provider = embedding_provider or MockEmbeddingProvider()
        self._vector_store = vector_store or VectorStore()

    async def retrieve(self, query_text: str, top_k: int = 5) -> list[RetrievedDocument]:
        """Perform hybrid retrieval using RRF fusion of lexical & semantic results."""
        # 1. Lexical Retrieval via Search Abstraction Layer
        search_query = SearchQuery(raw_query=query_text)
        lexical_page = await self._search_service.search(search_query)

        lexical_docs: list[RetrievedDocument] = [
            RetrievedDocument(
                id=h.id,
                entity_type=h.entity_type,
                title=h.title,
                content=h.highlight or h.title,
                score=h.score,
                retrieval_mode="lexical",
                metadata=h.metadata,
            )
            for h in lexical_page.hits
        ]

        # 2. Semantic Retrieval via Vector Store
        query_vector = await self._embedding_provider.embed_text(query_text)
        vector_matches = self._vector_store.search(query_vector, top_k=top_k)

        semantic_docs: list[RetrievedDocument] = [
            RetrievedDocument(
                id=m.document.id,
                entity_type=m.document.metadata.get("entity_type", "election"),
                title=m.document.metadata.get("title", m.document.text[:50]),
                content=m.document.text,
                score=m.similarity_score,
                retrieval_mode="semantic",
                metadata=m.document.metadata,
            )
            for m in vector_matches
        ]

        # 3. Reciprocal Rank Fusion (RRF)
        fused_scores: dict[str, float] = {}
        doc_map: dict[str, RetrievedDocument] = {}

        for rank, doc in enumerate(lexical_docs):
            doc_map[doc.id] = doc
            fused_scores[doc.id] = fused_scores.get(doc.id, 0.0) + (
                1.0 / (RRF_CONSTANT + rank + 1)
            )

        for rank, doc in enumerate(semantic_docs):
            if doc.id not in doc_map:
                doc_map[doc.id] = doc
            fused_scores[doc.id] = fused_scores.get(doc.id, 0.0) + (
                1.0 / (RRF_CONSTANT + rank + 1)
            )

        # Build fused result list
        fused_docs = []
        for doc_id, rrf_score in fused_scores.items():
            doc = doc_map[doc_id]
            doc.score = round(rrf_score, 5)
            fused_docs.append(doc)

        # Sort descending by fused RRF score
        sorted_docs = sorted(fused_docs, key=lambda d: d.score, reverse=True)
        return sorted_docs[:top_k]
