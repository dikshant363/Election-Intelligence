"""AI Intelligence Layer Application Service coordinator."""

from __future__ import annotations

import time
from collections.abc import AsyncGenerator
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.citation import CitationGenerator
from app.ai.evaluation import RAGEvaluator
from app.ai.exceptions import PromptGuardrailError
from app.ai.guardrails import AIGuardrails
from app.ai.prompts import PromptOrchestrator
from app.ai.providers import LLMRequest, llm_registry
from app.ai.retrieval import HybridRetriever, RetrievedDocument
from app.ai.schemas import (
    AIMetricsSchema,
    AIQueryRequestSchema,
    AIQueryResponseSchema,
    ProviderInfoSchema,
)


@dataclass
class PlatformAIMetrics:
    """Aggregated usage and performance metrics for the AI platform."""

    total_queries: int = 0
    total_tokens: int = 0
    total_latency_ms: float = 0.0
    sum_grounding_score: float = 0.0
    sum_citation_coverage: float = 0.0


class AIService:
    """
    AI Intelligence Service.
    Coordinates Guardrails, Hybrid Retrieval, Prompt Orchestration, LLM Generation,
    Source Attribution, and Performance Accounting.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._guardrails = AIGuardrails()
        self._retriever = HybridRetriever(session)
        self._prompt_orchestrator = PromptOrchestrator()
        self._evaluator = RAGEvaluator()
        self._registry = llm_registry
        self.metrics = PlatformAIMetrics()

    async def execute_query(
        self, request: AIQueryRequestSchema
    ) -> AIQueryResponseSchema:
        """Execute single-turn RAG query with safety guardrails & citations."""
        t0 = time.monotonic()

        # 1. Guardrail validation
        guard_res = self._guardrails.validate_prompt(request.prompt)
        if not guard_res.is_safe:
            raise PromptGuardrailError(guard_res.reason)

        clean_prompt = guard_res.sanitized_prompt

        # 2. Hybrid Retrieval (if RAG enabled)
        retrieved_docs: list[RetrievedDocument] = []
        if request.enable_rag:
            retrieved_docs = await self._retriever.retrieve(
                clean_prompt, top_k=request.top_k
            )

        # 3. Prompt Orchestration & Context Assembly
        system_prompt, user_prompt = self._prompt_orchestrator.prepare_rag_prompt(
            clean_prompt, retrieved_docs
        )

        # 4. LLM Generation via Provider Abstraction
        target_provider = request.provider or getattr(settings, "AI_PROVIDER", "gemini")
        provider = self._registry.get(target_provider)
        llm_req = LLMRequest(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=request.temperature,
        )
        llm_resp = await provider.generate(llm_req)

        # 5. Citation & Reasoning Trace Attribution
        attributed = CitationGenerator.generate(llm_resp.content, retrieved_docs)
        sanitized_answer = self._guardrails.sanitize_output(attributed.answer)

        latency_ms = (time.monotonic() - t0) * 1000.0

        # 6. Quantitative Evaluation
        eval_report = self._evaluator.evaluate(
            query=clean_prompt,
            attributed_resp=attributed,
            retrieved_docs=retrieved_docs,
            latency_ms=latency_ms,
            token_count=llm_resp.total_tokens,
            provider_name=provider.provider_name,
        )

        # Update metrics
        self.metrics.total_queries += 1
        self.metrics.total_tokens += llm_resp.total_tokens
        self.metrics.total_latency_ms += latency_ms
        self.metrics.sum_grounding_score += eval_report.grounding_score
        self.metrics.sum_citation_coverage += eval_report.citation_coverage

        return AIQueryResponseSchema(
            answer=sanitized_answer,
            provider=provider.provider_name,
            citations=attributed.citations,
            reasoning=attributed.reasoning,
            prompt_tokens=llm_resp.prompt_tokens,
            completion_tokens=llm_resp.completion_tokens,
            total_tokens=llm_resp.total_tokens,
            latency_ms=round(latency_ms, 2),
        )

    async def stream_query(
        self, request: AIQueryRequestSchema
    ) -> AsyncGenerator[str, None]:
        """Stream RAG response tokens asynchronously."""
        guard_res = self._guardrails.validate_prompt(request.prompt)
        if not guard_res.is_safe:
            raise PromptGuardrailError(guard_res.reason)

        retrieved_docs: list[RetrievedDocument] = []
        if request.enable_rag:
            retrieved_docs = await self._retriever.retrieve(
                guard_res.sanitized_prompt, top_k=request.top_k
            )

        system_prompt, user_prompt = self._prompt_orchestrator.prepare_rag_prompt(
            guard_res.sanitized_prompt, retrieved_docs
        )

        provider = self._registry.get(request.provider)
        llm_req = LLMRequest(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=request.temperature,
        )

        async for chunk in provider.generate_stream(llm_req):
            yield chunk

    def list_providers(self) -> list[ProviderInfoSchema]:
        """List registered LLM providers."""
        return [
            ProviderInfoSchema(
                name=p_name,
                provider_type="llm",
                is_available=True,
                default_model=self._registry.get(p_name).default_model,
            )
            for p_name in self._registry.list_providers()
        ]

    def get_metrics(self) -> AIMetricsSchema:
        """Get platform usage & quality metrics."""
        q_count = max(1, self.metrics.total_queries)
        return AIMetricsSchema(
            total_queries=self.metrics.total_queries,
            total_tokens=self.metrics.total_tokens,
            avg_latency_ms=round(self.metrics.total_latency_ms / q_count, 2),
            avg_grounding_score=round(self.metrics.sum_grounding_score / q_count, 4),
            avg_citation_coverage=round(self.metrics.sum_citation_coverage / q_count, 4),
        )
