"""Immutable Audit Trail logging for administrative, authentication, and security events."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from app.production.schemas import AuditRecordSchema


class AuditLogger:
    """Records immutable audit trail events for compliance and security forensics."""

    def __init__(self) -> None:
        self._audit_records: list[AuditRecordSchema] = []

    def log_event(  # noqa: PLR0913
        self,
        event_type: str,
        actor_id: str,
        action: str,
        resource: str,
        ip_address: str = "127.0.0.1",
        details: dict[str, Any] | None = None,
    ) -> AuditRecordSchema:
        record = AuditRecordSchema(
            event_id=f"aud_{str(uuid.uuid4())[:8]}",
            event_type=event_type,
            timestamp=datetime.now(UTC).isoformat(),
            actor_id=actor_id,
            action=action,
            resource=resource,
            ip_address=ip_address,
            details=details or {},
        )
        self._audit_records.append(record)
        return record

    def list_records(self, event_type: str | None = None) -> list[AuditRecordSchema]:
        if event_type:
            return [r for r in self._audit_records if r.event_type == event_type]
        return list(self._audit_records)


# Global audit logger
global_audit_logger = AuditLogger()
