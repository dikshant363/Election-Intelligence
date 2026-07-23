"""Source attribution, evidence references, and explainability trace generator."""

from __future__ import annotations

from dataclasses import dataclass

from app.ai.retrieval import RetrievedDocument
from app.ai.schemas import CitationSchema, ReasoningTraceSchema


@dataclass
class AttributedResponse:
    """Complete AI response adorned with source citations and explainability reasoning trace."""

    answer: str
    citations: list[CitationSchema]
    reasoning: ReasoningTraceSchema


class CitationGenerator:
    """Generates source citations and explainability traces from retrieved documents."""

    @staticmethod
    def generate(
        raw_answer: str, docs: list[RetrievedDocument]
    ) -> AttributedResponse:
        citations = [
            CitationSchema(
                document_id=doc.id,
                entity_type=doc.entity_type,
                title=doc.title,
                snippet=doc.content[:150],
                relevance_score=doc.score,
            )
            for doc in docs
        ]

        retrieved_entities = list({doc.entity_type for doc in docs})
        evidence_refs = [f"{doc.title} ({doc.id})" for doc in docs]

        reasoning = ReasoningTraceSchema(
            retrieved_entities=retrieved_entities,
            retrieval_strategy="hybrid_rrf",
            confidence_score=0.95 if docs else 0.5,
            evidence_references=evidence_refs,
        )

        return AttributedResponse(
            answer=raw_answer,
            citations=citations,
            reasoning=reasoning,
        )
