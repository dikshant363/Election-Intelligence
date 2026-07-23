"""Search result DTOs and pagination containers."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SearchHit:
    """A single matched item in search results."""

    id: str
    entity_type: str
    title: str
    subtitle: str = ""
    highlight: str = ""
    score: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchPage:
    """Paginated result container."""

    hits: list[SearchHit]
    total: int
    page: int
    page_size: int
    query: str = ""
    took_ms: float = 0.0
    next_cursor: str | None = None

    @property
    def total_pages(self) -> int:
        if self.page_size == 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1


@dataclass
class ElectionSearchResult:
    """Projection of ElectionModel search results."""

    id: uuid.UUID
    title: str
    election_type: str
    status: str
    start_date: str
    end_date: str
    highlight: str = ""
    score: float = 1.0


@dataclass
class CandidateSearchResult:
    """Projection of CandidateModel search results."""

    id: uuid.UUID
    name: str
    party_code: str | None
    constituency_code: str
    state_code: str
    highlight: str = ""
    score: float = 1.0


@dataclass
class PartySearchResult:
    """Projection of PoliticalPartyModel search results."""

    id: uuid.UUID
    name: str
    code: str
    symbol: str
    highlight: str = ""
    score: float = 1.0


@dataclass
class ConstituencySearchResult:
    """Projection of ConstituencyModel search results."""

    id: uuid.UUID
    name: str
    code: str
    state_code: str
    constituency_type: str
    highlight: str = ""
    score: float = 1.0
