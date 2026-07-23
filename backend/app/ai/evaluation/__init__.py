"""Evaluation framework for RAG quality, citation coverage, grounding score, and latency."""

from __future__ import annotations

from dataclasses import dataclass

from app.ai.citation import AttributedResponse
from app.ai.retrieval import RetrievedDocument


@dataclass
class EvaluationReport:
    """Quantitative evaluation metrics for an AI generation."""

    retrieval_precision: float
    retrieval_recall: float
    citation_coverage: float
    grounding_score: float
    latency_ms: float
    token_count: int
    provider_name: str


class RAGEvaluator:
    """Evaluates RAG generation accuracy, source grounding, and latency."""

    @staticmethod
    def evaluate(  # noqa: PLR0913
        query: str,  # noqa: ARG004
        attributed_resp: AttributedResponse,
        retrieved_docs: list[RetrievedDocument],
        expected_doc_ids: list[str] | None = None,
        latency_ms: float = 0.0,
        token_count: int = 0,
        provider_name: str = "mock",
    ) -> EvaluationReport:
        """Calculate precision, recall, grounding score, and citation coverage."""
        retrieved_ids = {d.id for d in retrieved_docs}

        # Precision & Recall
        if expected_doc_ids:
            expected_set = set(expected_doc_ids)
            intersection = retrieved_ids.intersection(expected_set)
            precision = round(len(intersection) / len(retrieved_ids), 4) if retrieved_ids else 0.0
            recall = round(len(intersection) / len(expected_set), 4) if expected_set else 1.0
        else:
            precision = 1.0 if retrieved_docs else 0.0
            recall = 1.0

        # Citation Coverage: % of retrieved docs cited in response
        cited_ids = {c.document_id for c in attributed_resp.citations}
        citation_coverage = (
            round(len(cited_ids) / len(retrieved_ids), 4) if retrieved_ids else 1.0
        )

        # Grounding Score: estimate based on evidence presence
        grounding_score = round((precision * 0.4) + (citation_coverage * 0.6), 4)

        return EvaluationReport(
            retrieval_precision=precision,
            retrieval_recall=recall,
            citation_coverage=citation_coverage,
            grounding_score=grounding_score,
            latency_ms=latency_ms,
            token_count=token_count,
            provider_name=provider_name,
        )
