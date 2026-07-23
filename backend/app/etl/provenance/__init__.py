"""Provenance and data lineage tracking for all imported records."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ProvenanceRecordModel(Base):
    """
    Tracks the full lineage of every production record back to its source import.

    Every record that enters the production database must have a corresponding
    ProvenanceRecord linking it to its ImportBatch, source file, checksum, and
    transformation history.
    """

    __tablename__ = "provenance_records"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    batch_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("import_batches.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    entity_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    entity_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    source_uri: Mapped[str] = mapped_column(String(1024), nullable=False)
    source_checksum: Mapped[str | None] = mapped_column(String(64), nullable=True)
    source_format: Mapped[str] = mapped_column(String(20), nullable=False)
    record_index: Mapped[int] = mapped_column(Integer, nullable=False)
    transformer_version: Mapped[str] = mapped_column(String(20), default="1.0", nullable=False)
    imported_by: Mapped[str | None] = mapped_column(String(150), nullable=True)
    approval_status: Mapped[str] = mapped_column(
        String(20), default="pending", index=True, nullable=False
    )
    approved_by: Mapped[str | None] = mapped_column(String(150), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    imported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        index=True,
        nullable=False,
    )
