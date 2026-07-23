"""Production Hardening Layer Application Service coordinator."""

from __future__ import annotations

from typing import Any

from app.production.audit import AuditLogger, global_audit_logger
from app.production.backup import BackupManager, global_backup_manager
from app.production.config import ConfigurationValidator
from app.production.deployment import DeploymentSafetyManager
from app.production.release import ReleaseManager
from app.production.sbom import SBOMGenerator
from app.production.schemas import (
    AuditRecordSchema,
    BackupMetadataSchema,
    ConfigValidationSchema,
    ReleaseChecklistSchema,
    SBOMSummarySchema,
    SecurityStatusSchema,
)
from app.production.secrets import SecretsProvider, global_secrets_provider
from app.production.security import SecurityHardener


class ProductionService:
    """
    Production Service coordinator.
    Manages security status, secrets verification, configuration fingerprints,
    snapshots, supply chain SBOM, audit records, and release checklists.
    """

    def __init__(
        self,
        secrets_provider: SecretsProvider | None = None,
        backup_manager: BackupManager | None = None,
        audit_logger: AuditLogger | None = None,
    ) -> None:
        self.secrets_provider = secrets_provider or global_secrets_provider
        self.backup_manager = backup_manager or global_backup_manager
        self.audit_logger = audit_logger or global_audit_logger

    def get_security_status(self) -> SecurityStatusSchema:
        """Get security header, CSP, and transport validation status."""
        return SecurityHardener.get_security_status()

    def validate_configuration(self) -> ConfigValidationSchema:
        """Validate startup environment configuration fingerprint."""
        return ConfigurationValidator.validate_configuration()

    def list_backups(self) -> list[BackupMetadataSchema]:
        """List database snapshot backup records."""
        return self.backup_manager.list_snapshots()

    def create_backup(self) -> BackupMetadataSchema:
        """Create new database snapshot record."""
        meta = self.backup_manager.create_snapshot()
        self.audit_logger.log_event(
            event_type="admin",
            actor_id="system",
            action="create_backup",
            resource=meta.backup_id,
        )
        return meta

    def list_audit_records(self, event_type: str | None = None) -> list[AuditRecordSchema]:
        """List immutable audit log trail records."""
        return self.audit_logger.list_records(event_type=event_type)

    def get_sbom_summary(self) -> SBOMSummarySchema:
        """Get Software Bill of Materials (SBOM) summary."""
        return SBOMGenerator.get_sbom_summary()

    def get_spdx_sbom(self) -> dict[str, Any]:
        """Get full SPDX-2.3 SBOM document dictionary."""
        return SBOMGenerator.generate_spdx_document()

    def get_release_checklist(self) -> ReleaseChecklistSchema:
        """Get CI/CD quality gate release checklist."""
        return ReleaseManager.get_release_checklist()

    def verify_migration_safety(self, migration_name: str) -> dict[str, Any]:
        """Verify database migration safety for zero-downtime release."""
        return DeploymentSafetyManager.verify_migration_safety(migration_name)
