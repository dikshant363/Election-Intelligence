"""Search, Discovery & Query Platform package root."""

from app.search.exceptions import (
    FilterError,
    GeospatialError,
    IndexError,
    InvalidQueryError,
    SearchBackendError,
    SearchException,
)
from app.search.queries import (
    FieldWeight,
    Pagination,
    ParsedQueryNode,
    QueryType,
    SearchOperator,
    SearchQuery,
)
from app.search.results import (
    CandidateSearchResult,
    ConstituencySearchResult,
    ElectionSearchResult,
    PartySearchResult,
    SearchHit,
    SearchPage,
)
from app.search.services import SearchService

__all__ = [
    "SearchException",
    "InvalidQueryError",
    "IndexError",
    "SearchBackendError",
    "FilterError",
    "GeospatialError",
    "SearchQuery",
    "QueryType",
    "SearchOperator",
    "Pagination",
    "FieldWeight",
    "ParsedQueryNode",
    "SearchHit",
    "SearchPage",
    "ElectionSearchResult",
    "CandidateSearchResult",
    "PartySearchResult",
    "ConstituencySearchResult",
    "SearchService",
]
