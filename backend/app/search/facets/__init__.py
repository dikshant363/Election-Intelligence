"""
Faceted search and aggregation engine.

Produces facet buckets for filtering UI and aggregated reporting queries.
All operations are read-only, parameterised SQL via SQLAlchemy Core.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models import (
    CandidateModel,
    ConstituencyModel,
    ElectionModel,
    PoliticalPartyModel,
)
from app.search.results import AggregationResult, FacetBucket, FacetResult


async def get_election_facets(session: AsyncSession) -> list[FacetResult]:
    """Return facet buckets for election_type and status dimensions."""
    facets: list[FacetResult] = []

    # Election type facet
    type_stmt = (
        select(ElectionModel.election_type, func.count(ElectionModel.id).label("cnt"))
        .where(ElectionModel.deleted_at.is_(None))
        .group_by(ElectionModel.election_type)
        .order_by(func.count(ElectionModel.id).desc())
    )
    type_rows = (await session.execute(type_stmt)).all()
    facets.append(
        FacetResult(
            field="election_type",
            buckets=[
                FacetBucket(value=r.election_type, label=r.election_type, count=r.cnt)
                for r in type_rows
            ],
        )
    )

    # Status facet
    status_stmt = (
        select(ElectionModel.status, func.count(ElectionModel.id).label("cnt"))
        .where(ElectionModel.deleted_at.is_(None))
        .group_by(ElectionModel.status)
        .order_by(func.count(ElectionModel.id).desc())
    )
    status_rows = (await session.execute(status_stmt)).all()
    facets.append(
        FacetResult(
            field="status",
            buckets=[
                FacetBucket(value=r.status, label=r.status, count=r.cnt)
                for r in status_rows
            ],
        )
    )

    return facets


async def get_constituency_facets(session: AsyncSession) -> list[FacetResult]:
    """Return facet buckets for state_code and constituency_type dimensions."""
    facets: list[FacetResult] = []

    state_stmt = (
        select(ConstituencyModel.state_code, func.count(ConstituencyModel.id).label("cnt"))
        .where(ConstituencyModel.deleted_at.is_(None))
        .group_by(ConstituencyModel.state_code)
        .order_by(func.count(ConstituencyModel.id).desc())
    )
    state_rows = (await session.execute(state_stmt)).all()
    facets.append(
        FacetResult(
            field="state_code",
            buckets=[
                FacetBucket(value=r.state_code, label=r.state_code, count=r.cnt)
                for r in state_rows
            ],
        )
    )

    type_stmt = (
        select(
            ConstituencyModel.constituency_type,
            func.count(ConstituencyModel.id).label("cnt"),
        )
        .where(ConstituencyModel.deleted_at.is_(None))
        .group_by(ConstituencyModel.constituency_type)
        .order_by(func.count(ConstituencyModel.id).desc())
    )
    type_rows = (await session.execute(type_stmt)).all()
    facets.append(
        FacetResult(
            field="constituency_type",
            buckets=[
                FacetBucket(
                    value=r.constituency_type,
                    label=r.constituency_type,
                    count=r.cnt,
                )
                for r in type_rows
            ],
        )
    )

    return facets


async def get_candidate_facets(session: AsyncSession) -> list[FacetResult]:
    """Return facet buckets for state_code dimension on candidates."""
    state_stmt = (
        select(ConstituencyModel.state_code, func.count(CandidateModel.id).label("cnt"))
        .join(ConstituencyModel, CandidateModel.constituency_id == ConstituencyModel.id)
        .where(CandidateModel.deleted_at.is_(None))
        .group_by(ConstituencyModel.state_code)
        .order_by(func.count(CandidateModel.id).desc())
    )
    rows = (await session.execute(state_stmt)).all()
    return [
        FacetResult(
            field="state_code",
            buckets=[
                FacetBucket(value=r.state_code, label=r.state_code, count=r.cnt)
                for r in rows
            ],
        )
    ]


async def aggregate_candidates_by_party(
    session: AsyncSession,
) -> AggregationResult:
    """Return candidate count grouped by party code."""
    stmt = (
        select(
            PoliticalPartyModel.code.label("party_code"),
            PoliticalPartyModel.name.label("party_name"),
            func.count(CandidateModel.id).label("candidate_count"),
        )
        .join(PoliticalPartyModel, CandidateModel.party_id == PoliticalPartyModel.id)
        .where(CandidateModel.deleted_at.is_(None))
        .group_by(PoliticalPartyModel.code, PoliticalPartyModel.name)
        .order_by(func.count(CandidateModel.id).desc())
    )
    rows = (await session.execute(stmt)).all()
    return AggregationResult(
        group_by=["party_code"],
        rows=[
            {
                "party_code": r.party_code,
                "party_name": r.party_name,
                "candidate_count": r.candidate_count,
            }
            for r in rows
        ],
        total_groups=len(rows),
    )


async def aggregate_constituencies_by_state(
    session: AsyncSession,
) -> AggregationResult:
    """Return constituency count grouped by state."""
    stmt = (
        select(
            ConstituencyModel.state_code,
            func.count(ConstituencyModel.id).label("constituency_count"),
        )
        .where(ConstituencyModel.deleted_at.is_(None))
        .group_by(ConstituencyModel.state_code)
        .order_by(func.count(ConstituencyModel.id).desc())
    )
    rows = (await session.execute(stmt)).all()
    return AggregationResult(
        group_by=["state_code"],
        rows=[
            {
                "state_code": r.state_code,
                "constituency_count": r.constituency_count,
            }
            for r in rows
        ],
        total_groups=len(rows),
    )


async def compute_data_quality_metrics(
    session: AsyncSession,
    entity: str,
) -> dict[str, Any]:
    """
    Compute automated data quality metrics for a given entity type.
    Returns completeness, null field rates, and an overall quality score.
    """
    metrics: dict[str, Any] = {"entity_type": entity}

    if entity == "election":
        total_stmt = select(func.count(ElectionModel.id)).where(
            ElectionModel.deleted_at.is_(None)
        )
        null_title = select(func.count(ElectionModel.id)).where(
            ElectionModel.deleted_at.is_(None), ElectionModel.title == ""
        )
        total = (await session.execute(total_stmt)).scalar_one()
        null_count = (await session.execute(null_title)).scalar_one()
        null_rate = null_count / total if total > 0 else 0.0
        quality_score = 1.0 - null_rate
        metrics.update(
            {
                "total_records": total,
                "complete_records": total - null_count,
                "null_field_rates": {"title": null_rate},
                "quality_score": round(quality_score, 4),
            }
        )

    elif entity == "candidate":
        total_stmt = select(func.count(CandidateModel.id)).where(
            CandidateModel.deleted_at.is_(None)
        )
        no_party_stmt = select(func.count(CandidateModel.id)).where(
            CandidateModel.deleted_at.is_(None),
            CandidateModel.party_id.is_(None),
        )
        total = (await session.execute(total_stmt)).scalar_one()
        no_party = (await session.execute(no_party_stmt)).scalar_one()
        no_party_rate = no_party / total if total > 0 else 0.0
        quality_score = 1.0 - (no_party_rate * 0.3)
        metrics.update(
            {
                "total_records": total,
                "complete_records": total - no_party,
                "null_field_rates": {"party_id": no_party_rate},
                "quality_score": round(quality_score, 4),
            }
        )

    elif entity == "constituency":
        total_stmt = select(func.count(ConstituencyModel.id)).where(
            ConstituencyModel.deleted_at.is_(None)
        )
        total = (await session.execute(total_stmt)).scalar_one()
        metrics.update(
            {
                "total_records": total,
                "complete_records": total,
                "null_field_rates": {},
                "quality_score": 1.0,
            }
        )

    else:
        metrics.update(
            {
                "total_records": 0,
                "complete_records": 0,
                "null_field_rates": {},
                "quality_score": 0.0,
            }
        )

    return metrics
