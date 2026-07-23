"""Pydantic schemas for AI Intelligence Layer API endpoints."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CitationSchema(BaseModel):
    """Source attribution citation schema."""

    model_config = ConfigDict(frozen=True)

    document_id: str
    entity_type: str
    title: str
    snippet: str
    relevance_score: float = 1.0


class ReasoningTraceSchema(BaseModel):
    """Explainability metadata and reasoning trace."""

    model_config = ConfigDict(frozen=True)

    retrieved_entities: list[str]
    retrieval_strategy: str = "hybrid_rrf"
    confidence_score: float = 0.95
    evidence_references: list[str]


class AIQueryRequestSchema(BaseModel):
    """Request model for single-turn AI query / RAG."""

    model_config = ConfigDict(frozen=True)

    prompt: str = Field(..., min_length=1, max_length=2000, description="User question")
    provider: str = Field(default="mock", description="mock, openai, gemini, claude, ollama")
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    enable_rag: bool = Field(default=True)
    top_k: int = Field(default=5, ge=1, le=20)


class ChatMessageSchema(BaseModel):
    """Chat conversation message."""

    model_config = ConfigDict(frozen=True)

    role: str = Field(..., description="system, user, assistant")
    content: str = Field(..., min_length=1)


class AIChatRequestSchema(BaseModel):
    """Request model for multi-turn AI chat."""

    model_config = ConfigDict(frozen=True)

    messages: list[ChatMessageSchema] = Field(..., min_length=1)
    provider: str = Field(default="mock")
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    enable_rag: bool = Field(default=True)


class AIQueryResponseSchema(BaseModel):
    """Response model for AI query / RAG."""

    model_config = ConfigDict(frozen=True)

    answer: str
    provider: str
    citations: list[CitationSchema]
    reasoning: ReasoningTraceSchema
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_ms: float = 0.0


class ProviderInfoSchema(BaseModel):
    """Provider availability information."""

    model_config = ConfigDict(frozen=True)

    name: str
    provider_type: str
    is_available: bool
    default_model: str


class AIMetricsSchema(BaseModel):
    """AI platform usage & evaluation metrics."""

    model_config = ConfigDict(frozen=True)

    total_queries: int
    total_tokens: int
    avg_latency_ms: float
    avg_grounding_score: float
    avg_citation_coverage: float
