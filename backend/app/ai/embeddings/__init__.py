"""Embedding Provider Abstraction (OpenAI, Gemini, SentenceTransformers, Mock)."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Abstract interface for text embedding generation."""

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Vector embedding dimension length."""

    @abstractmethod
    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding vector for single string."""

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embedding vectors for batch of strings."""


class MockEmbeddingProvider(EmbeddingProvider):
    """Deterministic Mock Embedding Provider for testing & dev."""

    def __init__(self, dim: int = 384) -> None:
        self._dim = dim

    @property
    def dimension(self) -> int:
        return self._dim

    async def embed_text(self, text: str) -> list[float]:
        # Generate pseudo-random deterministic vector based on text hash
        val = sum(ord(c) for c in text) % 100 / 100.0
        vec = [val] * self._dim
        # Normalize
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [await self.embed_text(t) for t in texts]


class OpenAIEmbeddings(EmbeddingProvider):
    """OpenAI text-embedding-3-small adapter stub."""

    def __init__(self, api_key: str = "mock", dim: int = 1536) -> None:
        self.api_key = api_key
        self._dim = dim

    @property
    def dimension(self) -> int:
        return self._dim

    async def embed_text(self, _text: str) -> list[float]:
        return [0.1] * self._dim

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [[0.1] * self._dim for _ in texts]


class GeminiEmbeddings(EmbeddingProvider):
    """Google Gemini text-embedding-004 adapter stub."""

    def __init__(self, api_key: str = "mock", dim: int = 768) -> None:
        self.api_key = api_key
        self._dim = dim

    @property
    def dimension(self) -> int:
        return self._dim

    async def embed_text(self, _text: str) -> list[float]:
        return [0.2] * self._dim

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [[0.2] * self._dim for _ in texts]
