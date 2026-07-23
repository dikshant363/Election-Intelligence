"""AI Intelligence Layer exception hierarchy."""

from __future__ import annotations


class AIException(Exception):
    """Base exception for all AI & RAG operations."""

    def __init__(self, message: str, code: str = "AI_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class ProviderNotFoundError(AIException):
    """Raised when a requested LLM or Embedding provider is not configured or registered."""

    def __init__(self, provider_name: str) -> None:
        super().__init__(f"LLM Provider '{provider_name}' not found or unavailable.", code="PROVIDER_NOT_FOUND")


class PromptGuardrailError(AIException):
    """Raised when a prompt violates safety guardrails or contains prompt injection."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="GUARDRAIL_VIOLATION")


class RetrievalError(AIException):
    """Raised when semantic or hybrid retrieval fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="RETRIEVAL_ERROR")


class TokenBudgetExceededError(AIException):
    """Raised when prompt context exceeds maximum token budget."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="TOKEN_BUDGET_EXCEEDED")
