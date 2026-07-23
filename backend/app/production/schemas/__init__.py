"""Pydantic v2 schemas for Production Hardening & Operations APIs."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SecurityStatusSchema(BaseModel):
    """Security status summary and header validation."""

    model_config = ConfigDict(frozen=True)

    headers_enforced: bool
    csp_enabled: bool
    hsts_enabled: bool
    cors_valid: bool
    secure_cookies: bool
    tls_enforced: bool


class ConfigValidationSchema(BaseModel):
    """Startup configuration validation report."""

    model_config = ConfigDict(frozen=True)

    status: str = Field(..., description="valid, invalid, warning")
    environment: str
    fingerprint: str
    missing_keys: list[str]
    invalid_keys: list[str]


class BackupMetadataSchema(BaseModel):
    """Database backup snapshot metadata."""

    model_config = ConfigDict(frozen=True)

    backup_id: str
    timestamp: str
    size_bytes: int
    checksum_sha256: str
    status: str = "completed"


class AuditRecordSchema(BaseModel):
    """Immutable audit trail record."""

    model_config = ConfigDict(frozen=True)

    event_id: str
    event_type: str = Field(..., description="admin, auth, config, security")
    timestamp: str
    actor_id: str
    action: str
    resource: str
    ip_address: str
    details: dict[str, Any] = Field(default_factory=dict)


class SBOMSummarySchema(BaseModel):
    """Software Bill of Materials (SBOM) summary."""

    model_config = ConfigDict(frozen=True)

    total_dependencies: int
    python_packages: int
    vulnerabilities_detected: int
    sbom_format: str = "SPDX-2.3"


class ReleaseChecklistSchema(BaseModel):
    """Pre-release readiness checklist and health status."""

    model_config = ConfigDict(frozen=True)

    version: str
    tests_passed: bool
    lint_passed: bool
    migrations_verified: bool
    security_verified: bool
    sbom_generated: bool
    ready_for_deployment: bool
