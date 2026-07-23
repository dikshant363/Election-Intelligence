"""Prompt orchestration, templates, context assembly, and token budgeting."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.ai.retrieval import RetrievedDocument

PROMPT_VERSION = "v1.0"
DEFAULT_TOKEN_BUDGET = 2000

SYSTEM_PROMPT_TEMPLATE = """You are the Election Intelligence AI Assistant, an authoritative system for analyzing official election data in India.
Answer the user's question using ONLY the provided verified context documents.
Always maintain strict neutrality, zero political bias, and cite your sources using document references.

Context Documents:
{context_str}
"""


@dataclass
class PromptTemplate:
    """Versioned prompt template."""

    name: str
    template: str
    version: str = PROMPT_VERSION

    def format(self, **kwargs: Any) -> str:
        return self.template.format(**kwargs)


class PromptOrchestrator:
    """Assembles prompt contexts, formats templates, and enforces token budgets."""

    def __init__(self, token_budget: int = DEFAULT_TOKEN_BUDGET) -> None:
        self.token_budget = token_budget

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Estimate token count (approx 4 chars per token)."""
        return max(1, len(text) // 4)

    def assemble_context(self, docs: list[RetrievedDocument]) -> str:
        """Assemble retrieved documents into structured context text."""
        if not docs:
            return "No relevant context documents retrieved."

        lines = []
        for i, doc in enumerate(docs, 1):
            lines.append(f"[{i}] [{doc.entity_type.upper()}] {doc.title}: {doc.content}")

        return "\n".join(lines)

    def prepare_rag_prompt(
        self, user_question: str, docs: list[RetrievedDocument]
    ) -> tuple[str, str]:
        """Prepare system prompt and formatted user prompt for RAG."""
        context_str = self.assemble_context(docs)
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context_str=context_str)

        total_tokens = self.estimate_tokens(system_prompt) + self.estimate_tokens(
            user_question
        )
        if total_tokens > self.token_budget:
            # Truncate context if budget exceeded
            truncated_docs = docs[: max(1, len(docs) // 2)]
            context_str = self.assemble_context(truncated_docs)
            system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context_str=context_str)

        return system_prompt, user_question
