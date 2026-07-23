"""SQLAlchemy model for PollingBooth aggregate."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.persistence.models.constituency import ConstituencyModel


class PollingBoothModel(BaseModel):
    """SQLAlchemy ORM model for polling_booths table."""

    __tablename__ = "polling_booths"

    constituency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("constituencies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    booth_name: Mapped[str] = mapped_column(String(255), nullable=False)
    booth_number: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    constituency: Mapped["ConstituencyModel"] = relationship(
        "ConstituencyModel",
        back_populates="polling_booths",
    )

    __table_args__ = (
        UniqueConstraint(
            "constituency_id",
            "booth_number",
            name="uq_polling_booths_constituency_booth_number",
        ),
        Index("ix_polling_booths_constituency_id", "constituency_id"),
    )
