"""Reusable aggregation and statistical analysis engine for election data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models import (
    CandidateModel,
    ConstituencyModel,
    ElectionModel,
    ElectionResultModel,
    PoliticalPartyModel,
    PollingBoothModel,
)


@dataclass
class AggregationMetric:
    """A statistical aggregation metric result."""

    metric_name: str
    group_by_fields: list[str]
    data: list[dict[str, Any]]
    total_groups: int = 0


class AnalyticsEngine:
    """Reusable statistical aggregation engine."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def count_by_state(self) -> AggregationMetric:
        """Count constituencies per state."""
        stmt = (
            select(
                ConstituencyModel.state_code,
                func.count(ConstituencyModel.id).label("count"),
            )
            .where(ConstituencyModel.deleted_at.is_(None))
            .group_by(ConstituencyModel.state_code)
            .order_by(func.count(ConstituencyModel.id).desc())
        )
        rows = (await self._session.execute(stmt)).all()
        data = [{"state_code": r.state_code, "count": r.count} for r in rows]
        return AggregationMetric(
            metric_name="constituency_count_by_state",
            group_by_fields=["state_code"],
            data=data,
            total_groups=len(data),
        )

    async def count_by_party(self) -> AggregationMetric:
        """Count candidates per political party."""
        stmt = (
            select(
                PoliticalPartyModel.code,
                PoliticalPartyModel.name,
                func.count(CandidateModel.id).label("candidate_count"),
            )
            .join(PoliticalPartyModel, CandidateModel.party_id == PoliticalPartyModel.id)
            .where(CandidateModel.deleted_at.is_(None))
            .group_by(PoliticalPartyModel.code, PoliticalPartyModel.name)
            .order_by(func.count(CandidateModel.id).desc())
        )
        rows = (await self._session.execute(stmt)).all()
        data = [
            {"party_code": r.code, "party_name": r.name, "candidate_count": r.candidate_count}
            for r in rows
        ]
        return AggregationMetric(
            metric_name="candidate_count_by_party",
            group_by_fields=["party_code"],
            data=data,
            total_groups=len(data),
        )

    async def count_by_election(self) -> AggregationMetric:
        """Count declared election results per election type."""
        stmt = (
            select(
                ElectionModel.election_type,
                func.count(ElectionResultModel.id).label("results_count"),
            )
            .join(ElectionModel, ElectionResultModel.election_id == ElectionModel.id)
            .group_by(ElectionModel.election_type)
        )
        rows = (await self._session.execute(stmt)).all()
        data = [
            {"election_type": r.election_type, "results_count": r.results_count}
            for r in rows
        ]
        return AggregationMetric(
            metric_name="results_count_by_election_type",
            group_by_fields=["election_type"],
            data=data,
            total_groups=len(data),
        )

    async def get_turnout_statistics(self) -> dict[str, Any]:
        """Compute platform-wide election turnout statistics."""
        elections_sub = select(func.count(ElectionModel.id)).scalar_subquery()
        candidates_sub = select(func.count(CandidateModel.id)).scalar_subquery()
        booths_sub = select(func.count(PollingBoothModel.id)).scalar_subquery()

        stmt = select(
            elections_sub.label("total_elections"),
            candidates_sub.label("total_candidates"),
            booths_sub.label("total_polling_booths"),
        )
        res = (await self._session.execute(stmt)).one()
        return {
            "total_elections": res.total_elections,
            "total_candidates": res.total_candidates,
            "total_polling_booths": res.total_polling_booths,
        }
