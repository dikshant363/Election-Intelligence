"""SQLAlchemy model for PoliticalParty aggregate."""

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.persistence.models.candidate import CandidateModel


class PoliticalPartyModel(BaseModel):
    """SQLAlchemy ORM model for political_parties table."""

    __tablename__ = "political_parties"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    code: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    symbol: Mapped[str] = mapped_column(String(255), nullable=False)

    candidates: Mapped[list["CandidateModel"]] = relationship(
        "CandidateModel",
        back_populates="party",
    )
