"""FastAPI router for security status, configuration validation, backup, audit trail, and release readiness."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies.dependencies import get_production_service
from app.production.schemas import (
    AuditRecordSchema,
    BackupMetadataSchema,
    ConfigValidationSchema,
    ReleaseChecklistSchema,
    SecurityStatusSchema,
)
from app.production.services import ProductionService

router = APIRouter(tags=["Production Hardening & Operations"])


@router.get(
    "/security",
    response_model=SecurityStatusSchema,
    status_code=status.HTTP_200_OK,
    summary="Get security hardening status (Headers, CSP, HSTS, TLS)",
)
async def security_status(
    prod_service: Annotated[ProductionService, Depends(get_production_service)],
) -> SecurityStatusSchema:
    """Return security status and header enforcement policies."""
    return prod_service.get_security_status()


@router.get(
    "/config",
    response_model=ConfigValidationSchema,
    status_code=status.HTTP_200_OK,
    summary="Get configuration fingerprint and startup validation status",
)
async def config_validation(
    prod_service: Annotated[ProductionService, Depends(get_production_service)],
) -> ConfigValidationSchema:
    """Return startup configuration fingerprint and required key validation."""
    return prod_service.validate_configuration()


@router.get(
    "/backup",
    response_model=list[BackupMetadataSchema],
    status_code=status.HTTP_200_OK,
    summary="List database snapshot backup records",
)
async def list_backups(
    prod_service: Annotated[ProductionService, Depends(get_production_service)],
) -> list[BackupMetadataSchema]:
    """Return list of snapshot backups."""
    return prod_service.list_backups()


@router.post(
    "/backup",
    response_model=BackupMetadataSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create new database snapshot backup record",
)
async def create_backup(
    prod_service: Annotated[ProductionService, Depends(get_production_service)],
) -> BackupMetadataSchema:
    """Trigger creation of a new database snapshot backup record with SHA-256 integrity hash."""
    return prod_service.create_backup()


@router.get(
    "/audit",
    response_model=list[AuditRecordSchema],
    status_code=status.HTTP_200_OK,
    summary="Get immutable audit trail records",
)
async def list_audit_records(
    event_type: Annotated[str | None, Query(description="Filter by type: admin, auth, config, security")] = None,
    prod_service: ProductionService = Depends(get_production_service),
) -> list[AuditRecordSchema]:
    """Return audit trail records filtered by event type."""
    return prod_service.list_audit_records(event_type=event_type)


@router.get(
    "/release",
    response_model=ReleaseChecklistSchema,
    status_code=status.HTTP_200_OK,
    summary="Get pre-release readiness checklist and CI/CD quality gates status",
)
async def release_checklist(
    prod_service: Annotated[ProductionService, Depends(get_production_service)],
) -> ReleaseChecklistSchema:
    """Return pre-release checklist and quality gate status."""
    return prod_service.get_release_checklist()
