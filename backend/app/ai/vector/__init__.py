"""Vector storage abstraction and in-memory cosine similarity search engine."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """Compute cosine similarity between two vector floats."""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2, strict=False))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


@dataclass
class VectorDocument:
    """Vector record container."""

    id: str
    text: str
    vector: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class VectorSearchResult:
    """Vector top-k search result match."""

    document: VectorDocument
    similarity_score: float


class VectorStore:
    """In-memory vector store with cosine similarity retrieval."""

    def __init__(self) -> None:
        self._documents: dict[str, VectorDocument] = {}

    def add_document(self, doc: VectorDocument) -> None:
        self._documents[doc.id] = doc

    def search(self, query_vector: list[float], top_k: int = 5) -> list[VectorSearchResult]:
        """Search top-k most similar vector documents."""
        results = []
        for doc in self._documents.values():
            sim = cosine_similarity(query_vector, doc.vector)
            results.append(VectorSearchResult(document=doc, similarity_score=round(sim, 4)))

        # Sort descending by similarity
        return sorted(results, key=lambda r: r.similarity_score, reverse=True)[:top_k]

    def clear(self) -> None:
        self._documents.clear()
