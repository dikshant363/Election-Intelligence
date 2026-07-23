"""Declarative base and foundation model class."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.database.metadata import metadata


class Base(DeclarativeBase):
    """Base declarative class for all SQLAlchemy models."""

    metadata: MetaData = metadata


class BaseModel(Base):
    """Abstract base model with standard columns for auditability and consistency.

    Includes UUID primary key, timestamping, soft delete support, and versioning.
    """

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        sort_order=-10,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )
