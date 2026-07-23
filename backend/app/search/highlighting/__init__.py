"""Highlighting generator for matched query terms in text fields."""

from __future__ import annotations

import re
from dataclasses import dataclass

DEFAULT_FRAGMENT_SIZE = 150
DEFAULT_PRE_TAG = "<mark>"
DEFAULT_POST_TAG = "</mark>"


@dataclass
class HighlightConfig:
    """Configuration for text snippet highlighting."""

    pre_tag: str = DEFAULT_PRE_TAG
    post_tag: str = DEFAULT_POST_TAG
    fragment_size: int = DEFAULT_FRAGMENT_SIZE
    max_fragments: int = 3


class TextHighlighter:
    """Generates highlighted text snippets with HTML/XML tags around matched terms."""

    def __init__(self, config: HighlightConfig | None = None) -> None:
        self.config = config or HighlightConfig()

    def highlight_terms(self, text: str, query_terms: list[str]) -> str:
        """Wrap matching terms in text with pre_tag and post_tag."""
        if not text or not query_terms:
            return text

        clean_terms = [re.escape(t.strip()) for t in query_terms if t.strip()]
        if not clean_terms:
            return text

        pattern = re.compile(r"\b(" + "|".join(clean_terms) + r")\b", re.IGNORECASE)

        def _replace(match: re.Match[str]) -> str:
            return f"{self.config.pre_tag}{match.group(0)}{self.config.post_tag}"

        return pattern.sub(_replace, text)

    def extract_snippet(self, text: str, query_terms: list[str]) -> str:
        """Extract a snippet of text centered around the first matching term."""
        if not text:
            return ""
        if not query_terms:
            return text[: self.config.fragment_size] + (
                "..." if len(text) > self.config.fragment_size else ""
            )

        clean_terms = [re.escape(t.strip()) for t in query_terms if t.strip()]
        if not clean_terms:
            return text[: self.config.fragment_size]

        pattern = re.compile(r"\b(" + "|".join(clean_terms) + r")\b", re.IGNORECASE)
        match = pattern.search(text)

        if not match:
            return text[: self.config.fragment_size] + (
                "..." if len(text) > self.config.fragment_size else ""
            )

        start = max(0, match.start() - self.config.fragment_size // 2)
        end = min(len(text), start + self.config.fragment_size)

        snippet = text[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."

        return self.highlight_terms(snippet, query_terms)
