"""Search exception hierarchy."""

from __future__ import annotations


class SearchException(Exception):
    """Base exception for all search operations."""

    def __init__(self, message: str, code: str = "SEARCH_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class InvalidQueryError(SearchException):
    """Raised when a search query is malformed or invalid."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="INVALID_QUERY")


class IndexError(SearchException):
    """Raised when a full-text search index operation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="INDEX_ERROR")


class SearchBackendError(SearchException):
    """Raised when a search engine backend fails or is unreachable."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="SEARCH_BACKEND_ERROR")


class FilterError(SearchException):
    """Raised when filter construction or application fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="FILTER_ERROR")


class GeospatialError(SearchException):
    """Raised when geospatial query parameters are out of bounds or invalid."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="GEOSPATIAL_ERROR")
