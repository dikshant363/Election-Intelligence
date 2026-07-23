"""FastAPI router for /api/v1/ai endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from app.ai.schemas import (
    AIChatRequestSchema,
    AIMetricsSchema,
    AIQueryRequestSchema,
    AIQueryResponseSchema,
    ProviderInfoSchema,
)
from app.ai.services import AIService
from app.api.v1.dependencies.dependencies import get_ai_service

router = APIRouter(prefix="/ai", tags=["AI Intelligence"])


@router.post(
    "/query",
    response_model=AIQueryResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Execute RAG question-answering query",
)
async def query(
    body: AIQueryRequestSchema,
    ai_service: Annotated[AIService, Depends(get_ai_service)],
) -> AIQueryResponseSchema:
    """Execute RAG query with source citations and explainability reasoning."""
    return await ai_service.execute_query(body)


@router.post(
    "/chat",
    response_model=AIQueryResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Execute multi-turn RAG chat",
)
async def chat(
    body: AIChatRequestSchema,
    ai_service: Annotated[AIService, Depends(get_ai_service)],
) -> AIQueryResponseSchema:
    """Execute multi-turn conversation RAG query."""
    last_msg = body.messages[-1].content
    query_req = AIQueryRequestSchema(
        prompt=last_msg,
        provider=body.provider,
        temperature=body.temperature,
        enable_rag=body.enable_rag,
    )
    return await ai_service.execute_query(query_req)


@router.post(
    "/stream",
    status_code=status.HTTP_200_OK,
    summary="Stream RAG response tokens via SSE",
)
async def stream(
    body: AIQueryRequestSchema,
    ai_service: Annotated[AIService, Depends(get_ai_service)],
) -> StreamingResponse:
    """Stream AI completion tokens asynchronously."""
    generator = ai_service.stream_query(body)
    return StreamingResponse(generator, media_type="text/event-stream")


@router.get(
    "/providers",
    response_model=list[ProviderInfoSchema],
    status_code=status.HTTP_200_OK,
    summary="List available LLM providers",
)
async def list_providers(
    ai_service: Annotated[AIService, Depends(get_ai_service)],
) -> list[ProviderInfoSchema]:
    """Return list of configured LLM providers."""
    return ai_service.list_providers()


@router.get(
    "/metrics",
    response_model=AIMetricsSchema,
    status_code=status.HTTP_200_OK,
    summary="Get AI platform quality & performance metrics",
)
async def metrics(
    ai_service: Annotated[AIService, Depends(get_ai_service)],
) -> AIMetricsSchema:
    """Get aggregated usage, grounding score, and citation coverage metrics."""
    return ai_service.get_metrics()
