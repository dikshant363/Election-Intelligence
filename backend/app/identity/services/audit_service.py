"""Audit logging service for tracking security events."""

import json
import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.identity.models.audit import AuditEntryModel


class AuditService:
    """Service writing immutable audit log records to PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def log_event(
        self,
        action: str,
        resource: str,
        user_id: uuid.UUID | None = None,
        ip_address: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> AuditEntryModel:
        """Write an immutable audit log entry to database."""
        details_json = json.dumps(details) if details else None
        entry = AuditEntryModel(
            user_id=user_id,
            action=action,
            resource=resource,
            ip_address=ip_address,
            details=details_json,
        )
        self._session.add(entry)
        await self._session.flush()
        return entry
