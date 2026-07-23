"""Search query domain models and query AST."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

# Query parameter boundary constants
MAX_PAGE_SIZE = 100
MIN_PAGE_SIZE = 1
MIN_PAGE = 1
MAX_QUERY_LEN = 500


class SearchOperator(StrEnum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


class QueryType(StrEnum):
    BOOLEAN = "boolean"
    PHRASE = "phrase"
    PREFIX = "prefix"
    FUZZY = "fuzzy"
    FIELD_SPECIFIC = "field_specific"
    MULTI_FIELD = "multi_field"


@dataclass
class Pagination:
    """Pagination configuration for search results."""

    page: int = 1
    page_size: int = 20
    cursor: str | None = None

    def __post_init__(self) -> None:
        self.page = max(self.page, MIN_PAGE)
        self.page_size = max(min(self.page_size, MAX_PAGE_SIZE), MIN_PAGE_SIZE)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


@dataclass
class FieldWeight:
    """Weight boost configuration for a specific field."""

    field_name: str
    weight: float = 1.0


@dataclass
class SearchQuery:
    """Universal search query object supporting complex queries."""

    raw_query: str = ""
    query_type: QueryType = QueryType.BOOLEAN
    operator: SearchOperator = SearchOperator.AND
    fields: list[str] = field(default_factory=list)
    field_weights: dict[str, float] = field(default_factory=dict)
    fuzziness: int = 1  # Levenshtein distance for fuzzy queries
    is_phrase: bool = False
    filters: dict[str, Any] = field(default_factory=dict)
    pagination: Pagination = field(default_factory=Pagination)
    enable_highlighting: bool = True
    enable_cache: bool = True

    def __post_init__(self) -> None:
        self.raw_query = self.raw_query.strip()[:MAX_QUERY_LEN]


@dataclass
class ParsedQueryNode:
    """Node in parsed query Abstract Syntax Tree (AST)."""

    token: str
    field_name: str | None = None
    operator: SearchOperator = SearchOperator.AND
    is_prefix: bool = False
    is_fuzzy: bool = False
    boost: float = 1.0
    children: list[ParsedQueryNode] = field(default_factory=list)
