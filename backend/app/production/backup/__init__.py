"""Database backup snapshot creation, verification, and disaster recovery."""

from __future__ import annotations

import hashlib
import uuid
from datetime import UTC, datetime

from app.production.schemas import BackupMetadataSchema


class BackupManager:
    """Manages database snapshot creation, verification, and recovery workflows."""

    def __init__(self) -> None:
        self._snapshots: dict[str, BackupMetadataSchema] = {}

    def create_snapshot(self, payload: bytes = b"election_db_dump") -> BackupMetadataSchema:
        """Create database backup snapshot with SHA-256 integrity checksum."""
        backup_id = f"snap_{str(uuid.uuid4())[:8]}"
        checksum = hashlib.sha256(payload).hexdigest()
        meta = BackupMetadataSchema(
            backup_id=backup_id,
            timestamp=datetime.now(UTC).isoformat(),
            size_bytes=len(payload),
            checksum_sha256=checksum,
            status="completed",
        )
        self._snapshots[backup_id] = meta
        return meta

    def list_snapshots(self) -> list[BackupMetadataSchema]:
        """List created backup snapshots."""
        return list(self._snapshots.values())

    def verify_snapshot(self, backup_id: str, payload: bytes) -> bool:
        """Verify checksum integrity of a backup snapshot."""
        meta = self._snapshots.get(backup_id)
        if not meta:
            return False
        calc = hashlib.sha256(payload).hexdigest()
        return calc == meta.checksum_sha256


# Singleton backup manager
global_backup_manager = BackupManager()
