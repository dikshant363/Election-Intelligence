"""Reusable filter components for election intelligence search."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from sqlalchemy import and_, or_
from sqlalchemy.sql.elements import BinaryExpression

from app.search.exceptions import FilterError


@dataclass
class FilterCriterion:
    """A single filter criterion."""

    field_name: str
    operator: str  # eq, in, range, gte, lte, like
    value: Any


@dataclass
class SearchFilterSet:
    """Set of filters that can be arbitrarily combined."""

    election_id: str | None = None
    state_code: str | None = None
    district: str | None = None
    constituency_code: str | None = None
    party_code: str | None = None
    candidate_id: str | None = None
    gender: str | None = None
    election_year: int | None = None
    election_type: str | None = None
    status: str | None = None
    date_from: date | None = None
    date_to: date | None = None
    additional_filters: list[FilterCriterion] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert active filters to dictionary."""
        res: dict[str, Any] = {}
        for key in (
            "election_id",
            "state_code",
            "district",
            "constituency_code",
            "party_code",
            "candidate_id",
            "gender",
            "election_year",
            "election_type",
            "status",
        ):
            val = getattr(self, key)
            if val is not None:
                res[key] = val
        if self.date_from:
            res["date_from"] = self.date_from.isoformat()
        if self.date_to:
            res["date_to"] = self.date_to.isoformat()
        return res

    def validate(self) -> None:
        """Validate filter parameter consistency."""
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise FilterError("date_from cannot be after date_to")
        if self.election_year is not None and (
            self.election_year < 1947 or self.election_year > 2100  # noqa: PLR2004
        ):
            raise FilterError(f"Invalid election_year: {self.election_year}")


class SQLFilterBuilder:
    """Builds SQLAlchemy expressions from a SearchFilterSet."""

    @staticmethod
    def build_election_conditions(model: Any, filters: SearchFilterSet) -> list[BinaryExpression[bool]]:
        """Build SQLAlchemy filter conditions for ElectionModel."""
        conditions = []
        if filters.election_type:
            conditions.append(model.election_type == filters.election_type)
        if filters.status:
            conditions.append(model.status == filters.status)
        if filters.date_from:
            conditions.append(model.start_date >= filters.date_from)
        if filters.date_to:
            conditions.append(model.end_date <= filters.date_to)
        return conditions

    @staticmethod
    def combine_conditions(conditions: list[Any], use_or: bool = False) -> Any:
        """Combine conditions with AND or OR logic."""
        if not conditions:
            return True
        return or_(*conditions) if use_or else and_(*conditions)
