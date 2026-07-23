"""Entity-specific typeahead autocomplete engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models import (
    CandidateModel,
    ConstituencyModel,
    ElectionModel,
    PoliticalPartyModel,
)

DEFAULT_TOP_N = 10


@dataclass
class AutocompleteSuggestion:
    """A single autocomplete suggestion item."""

    id: str
    label: str
    entity_type: str
    secondary: str = ""
    payload: dict[str, Any] | None = None


class AutocompleteEngine:
    """Provides fast prefix suggestions across candidates, parties, constituencies, and elections."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def suggest_candidates(
        self, prefix: str, limit: int = DEFAULT_TOP_N
    ) -> list[AutocompleteSuggestion]:
        """Suggest candidates matching name prefix."""
        stmt = (
            select(CandidateModel.id, CandidateModel.name)
            .where(CandidateModel.name.ilike(f"{prefix}%"))
            .where(CandidateModel.deleted_at.is_(None))
            .limit(limit)
        )
        rows = (await self._session.execute(stmt)).all()
        return [
            AutocompleteSuggestion(
                id=str(r.id),
                label=r.name,
                entity_type="candidate",
            )
            for r in rows
        ]

    async def suggest_parties(
        self, prefix: str, limit: int = DEFAULT_TOP_N
    ) -> list[AutocompleteSuggestion]:
        """Suggest political parties matching name or party code prefix."""
        pattern = f"{prefix}%"
        stmt = (
            select(
                PoliticalPartyModel.id,
                PoliticalPartyModel.name,
                PoliticalPartyModel.code,
            )
            .where(
                or_(
                    PoliticalPartyModel.name.ilike(pattern),
                    PoliticalPartyModel.code.ilike(pattern),
                )
            )
            .limit(limit)
        )
        rows = (await self._session.execute(stmt)).all()
        return [
            AutocompleteSuggestion(
                id=str(r.id),
                label=r.name,
                entity_type="party",
                secondary=r.code,
            )
            for r in rows
        ]

    async def suggest_constituencies(
        self, prefix: str, limit: int = DEFAULT_TOP_N
    ) -> list[AutocompleteSuggestion]:
        """Suggest constituencies matching name or code prefix."""
        pattern = f"{prefix}%"
        stmt = (
            select(
                ConstituencyModel.id,
                ConstituencyModel.name,
                ConstituencyModel.code,
                ConstituencyModel.state_code,
            )
            .where(
                or_(
                    ConstituencyModel.name.ilike(pattern),
                    ConstituencyModel.code.ilike(pattern),
                )
            )
            .where(ConstituencyModel.deleted_at.is_(None))
            .limit(limit)
        )
        rows = (await self._session.execute(stmt)).all()
        return [
            AutocompleteSuggestion(
                id=str(r.id),
                label=r.name,
                entity_type="constituency",
                secondary=f"{r.code} ({r.state_code})",
            )
            for r in rows
        ]

    async def suggest_elections(
        self, prefix: str, limit: int = DEFAULT_TOP_N
    ) -> list[AutocompleteSuggestion]:
        """Suggest elections matching title prefix."""
        stmt = (
            select(
                ElectionModel.id,
                ElectionModel.title,
                ElectionModel.election_type,
            )
            .where(ElectionModel.title.ilike(f"{prefix}%"))
            .where(ElectionModel.deleted_at.is_(None))
            .limit(limit)
        )
        rows = (await self._session.execute(stmt)).all()
        return [
            AutocompleteSuggestion(
                id=str(r.id),
                label=r.title,
                entity_type="election",
                secondary=r.election_type,
            )
            for r in rows
        ]
