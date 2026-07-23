"""FastAPI router for health checks, Prometheus metrics exposition, diagnostics, and alerts."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.api.v1.dependencies.dependencies import get_observability_service
from app.observability.schemas import (
    AlertRuleSchema,
    DiagnosticsResponseSchema,
    HealthResponseSchema,
)
from app.observability.services import ObservabilityService

router = APIRouter(tags=["Observability & Operations"])


@router.get(
    "/health",
    response_model=HealthResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get overall platform health and component dependencies status",
)
async def health(
    obs_service: Annotated[ObservabilityService, Depends(get_observability_service)],
) -> HealthResponseSchema:
    """Evaluate readiness status across database, search, event bus, and AI providers."""
    return await obs_service.get_readiness()


@router.get(
    "/ready",
    response_model=HealthResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Platform readiness probe endpoint",
)
async def ready(
    obs_service: Annotated[ObservabilityService, Depends(get_observability_service)],
) -> HealthResponseSchema:
    """Readiness probe for Kubernetes/cloud load balancer routing."""
    return await obs_service.get_readiness()


@router.get(
    "/live",
    response_model=HealthResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Platform liveness probe endpoint",
)
async def live(
    obs_service: Annotated[ObservabilityService, Depends(get_observability_service)],
) -> HealthResponseSchema:
    """Liveness probe returning instant operational status."""
    return await obs_service.get_liveness()


@router.get(
    "/metrics",
    status_code=status.HTTP_200_OK,
    summary="Expose metrics in standard Prometheus text exposition format",
)
async def metrics(
    obs_service: Annotated[ObservabilityService, Depends(get_observability_service)],
) -> Response:
    """Return system & application metrics for Prometheus scraping."""
    prom_data = obs_service.get_prometheus_metrics()
    return Response(content=prom_data, media_type="text/plain; version=0.0.4; charset=utf-8")


@router.get(
    "/diagnostics",
    response_model=DiagnosticsResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get runtime diagnostics and feature flag status",
)
async def diagnostics(
    obs_service: Annotated[ObservabilityService, Depends(get_observability_service)],
) -> DiagnosticsResponseSchema:
    """Return environment status, uptime, worker flags, and feature toggles."""
    return obs_service.get_diagnostics()


@router.get(
    "/alerts",
    response_model=list[AlertRuleSchema],
    status_code=status.HTTP_200_OK,
    summary="Get active alert rules and firing status",
)
async def alerts(
    obs_service: Annotated[ObservabilityService, Depends(get_observability_service)],
) -> list[AlertRuleSchema]:
    """Return list of alert rules and firing conditions."""
    return obs_service.get_alerts()
