"""SQLAlchemy model for ElectionResult aggregate."""

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.persistence.models.candidate import CandidateModel
    from app.persistence.models.constituency import ConstituencyModel
    from app.persistence.models.election import ElectionModel


class ElectionResultModel(BaseModel):
    """SQLAlchemy ORM model for election_results table."""

    __tablename__ = "election_results"

    result_key: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    election_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("elections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    constituency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("constituencies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    winning_candidate_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("candidates.id", ondelete="SET NULL"),
        nullable=True,
    )
    total_votes: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    candidate_votes_json: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    is_declared: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    election: Mapped["ElectionModel"] = relationship(
        "ElectionModel",
        back_populates="results",
    )
    constituency: Mapped["ConstituencyModel"] = relationship(
        "ConstituencyModel",
        back_populates="results",
    )
    winning_candidate: Mapped["CandidateModel | None"] = relationship(
        "CandidateModel",
    )

    __table_args__ = (
        UniqueConstraint(
            "election_id",
            "constituency_id",
            name="uq_election_results_election_constituency",
        ),
        Index("ix_election_results_election_constituency", "election_id", "constituency_id"),
    )
