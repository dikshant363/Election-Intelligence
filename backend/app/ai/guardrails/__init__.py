"""Prompt injection detection, safety guardrails, and PII filtering hooks."""

from __future__ import annotations

import re
from dataclasses import dataclass

# Known prompt injection attack signatures
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"system\s+prompt",
    r"disregard\s+above",
    r"you\s+are\s+now\s+a",
    r"jailbreak",
    r"override\s+rules",
    r"dan\s+mode",
]

_INJECTION_RE = re.compile("|".join(INJECTION_PATTERNS), re.IGNORECASE)


@dataclass
class GuardrailResult:
    """Outcome of safety guardrail evaluation."""

    is_safe: bool
    reason: str = ""
    sanitized_prompt: str = ""


class AIGuardrails:
    """Safety guardrail scanner for prompt injection, max lengths, and PII."""

    def __init__(self, max_prompt_len: int = 2000) -> None:
        self.max_prompt_len = max_prompt_len

    def validate_prompt(self, prompt: str) -> GuardrailResult:
        """Validate prompt against injection patterns and length limits."""
        if not prompt or not prompt.strip():
            return GuardrailResult(is_safe=False, reason="Prompt is empty.")

        if len(prompt) > self.max_prompt_len:
            return GuardrailResult(
                is_safe=False,
                reason=f"Prompt exceeds max length of {self.max_prompt_len} characters.",
            )

        match = _INJECTION_RE.search(prompt)
        if match:
            return GuardrailResult(
                is_safe=False,
                reason=f"Potential prompt injection detected matching pattern: '{match.group(0)}'",
            )

        return GuardrailResult(is_safe=True, sanitized_prompt=prompt.strip())

    def sanitize_output(self, text: str) -> str:
        """Sanitize LLM output text (e.g. scrub email/PII patterns if present)."""
        # Basic PII email scrubbing example
        return re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED_EMAIL]", text)
