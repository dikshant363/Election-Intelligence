"""SQLAlchemy model for Candidate aggregate."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.persistence.models.constituency import ConstituencyModel
    from app.persistence.models.party import PoliticalPartyModel


class CandidateModel(BaseModel):
    """SQLAlchemy ORM model for candidates table."""

    __tablename__ = "candidates"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    phone: Mapped[str] = mapped_column(String(50), nullable=False)

    constituency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("constituencies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    party_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("political_parties.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    constituency: Mapped["ConstituencyModel"] = relationship(
        "ConstituencyModel",
        back_populates="candidates",
    )
    party: Mapped["PoliticalPartyModel | None"] = relationship(
        "PoliticalPartyModel",
        back_populates="candidates",
    )

    __table_args__ = (
        Index("ix_candidates_constituency_party", "constituency_id", "party_id"),
    )
