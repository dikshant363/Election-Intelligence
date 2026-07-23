"""SQLAlchemy ORM models for ETL staging tables: ImportBatch, ImportRecord, RejectedRecord, TransformationLog."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class BatchStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    VALIDATING = "validating"
    TRANSFORMING = "transforming"
    LOADING = "loading"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ImportBatchModel(Base):
    """Tracks the lifecycle of a single import operation."""

    __tablename__ = "import_batches"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    job_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    source_uri: Mapped[str] = mapped_column(String(1024), nullable=False)
    source_checksum: Mapped[str | None] = mapped_column(String(64), nullable=True)
    format: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default=BatchStatus.PENDING, index=True, nullable=False
    )
    total_records: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    valid_records: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    rejected_records: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    loaded_records: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    initiated_by: Mapped[str | None] = mapped_column(String(150), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class ImportRecordModel(Base):
    """Represents a single staged record within an import batch."""

    __tablename__ = "import_records"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    batch_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("import_batches.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    record_index: Mapped[int] = mapped_column(Integer, nullable=False)
    raw_data: Mapped[str] = mapped_column(Text, nullable=False)
    transformed_data: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_loaded: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class RejectedRecordModel(Base):
    """Captures records that failed validation with structured error details."""

    __tablename__ = "rejected_records"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    batch_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("import_batches.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    record_index: Mapped[int] = mapped_column(Integer, nullable=False)
    raw_data: Mapped[str] = mapped_column(Text, nullable=False)
    error_code: Mapped[str] = mapped_column(String(50), nullable=False)
    error_message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class TransformationLogModel(Base):
    """Immutable audit record capturing every transformation applied to a batch."""

    __tablename__ = "transformation_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    batch_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("import_batches.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    transformer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    fields_transformed: Mapped[str] = mapped_column(Text, nullable=False)
    records_affected: Mapped[int] = mapped_column(Integer, nullable=False)
    applied_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
