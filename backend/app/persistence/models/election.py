"""SQLAlchemy model for Election aggregate."""

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.persistence.models.results import ElectionResultModel


class ElectionModel(BaseModel):
    """SQLAlchemy ORM model for elections table."""

    __tablename__ = "elections"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    election_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    results: Mapped[list["ElectionResultModel"]] = relationship(
        "ElectionResultModel",
        back_populates="election",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("ix_elections_type_status", "election_type", "status"),
    )
