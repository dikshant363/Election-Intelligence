"""SQLAlchemy ORM model for AuditEntry."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class AuditEntryModel(Base):
    """SQLAlchemy ORM model for immutable audit log entries."""

    __tablename__ = "audit_entries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True, nullable=True
    )
    action: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    resource: Mapped[str] = mapped_column(String(150), nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), index=True, nullable=False
    )
