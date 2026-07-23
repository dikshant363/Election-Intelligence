"""SQLAlchemy model for Constituency aggregate."""

from typing import TYPE_CHECKING

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.persistence.models.candidate import CandidateModel
    from app.persistence.models.polling import PollingBoothModel
    from app.persistence.models.results import ElectionResultModel


class ConstituencyModel(BaseModel):
    """SQLAlchemy ORM model for constituencies table."""

    __tablename__ = "constituencies"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    code: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    state_code: Mapped[str] = mapped_column(
        String(10), nullable=False, index=True
    )
    constituency_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="ASSEMBLY"
    )

    polling_booths: Mapped[list["PollingBoothModel"]] = relationship(
        "PollingBoothModel",
        back_populates="constituency",
        cascade="all, delete-orphan",
    )
    candidates: Mapped[list["CandidateModel"]] = relationship(
        "CandidateModel",
        back_populates="constituency",
    )
    results: Mapped[list["ElectionResultModel"]] = relationship(
        "ElectionResultModel",
        back_populates="constituency",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("ix_constituencies_state_code", "state_code"),
    )
