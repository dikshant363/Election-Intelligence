"""Relevance ranking, field boosting, and scoring algorithms."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class RankingConfig:
    """Configurable scoring & ranking configuration."""

    title_boost: float = 3.0
    name_boost: float = 2.5
    code_boost: float = 2.0
    body_boost: float = 1.0
    recency_boost_factor: float = 0.1  # Decay rate per year
    popularity_boost_factor: float = 0.05
    enable_recency: bool = True
    enable_popularity: bool = True


@dataclass
class ScoredHit:
    """A search hit adorned with calculated relevance score details."""

    id: str
    entity_type: str
    title: str
    raw_score: float
    highlight: str = ""
    field_boost: float = 1.0
    recency_boost: float = 1.0
    popularity_boost: float = 1.0
    final_score: float = 0.0
    metadata: dict = field(default_factory=dict)

    def calculate_final_score(self) -> float:
        self.final_score = round(
            self.raw_score * self.field_boost * self.recency_boost * self.popularity_boost,
            4,
        )
        return self.final_score


class RelevanceRanker:
    """Calculates final scores for search hits using configured boosts."""

    def __init__(self, config: RankingConfig | None = None) -> None:
        self.config = config or RankingConfig()

    def calculate_recency_boost(self, item_date: datetime | None) -> float:
        """Calculate exponential decay recency boost based on age in years."""
        if not self.config.enable_recency or not item_date:
            return 1.0
        now = datetime.now(UTC)
        age_years = max((now - item_date).days / 365.25, 0.0)
        # Boost decays towards 1.0 as age increases
        return round(1.0 + (1.0 / (1.0 + self.config.recency_boost_factor * age_years)), 4)

    def calculate_popularity_boost(self, view_count: int = 0) -> float:
        """Calculate logarithmic popularity boost based on interaction/view count."""
        if not self.config.enable_popularity or view_count <= 0:
            return 1.0

        return round(1.0 + self.config.popularity_boost_factor * math.log1p(view_count), 4)

    def rank_hits(self, hits: list[ScoredHit]) -> list[ScoredHit]:
        """Rank and sort a list of ScoredHits in descending order of final score."""
        for hit in hits:
            hit.calculate_final_score()
        return sorted(hits, key=lambda h: h.final_score, reverse=True)
