"""Observability Layer Application Service coordinator."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.observability.alerts import AlertManager, global_alert_manager
from app.observability.diagnostics import DiagnosticsProvider
from app.observability.health import HealthChecker
from app.observability.metrics import SystemMetricsRegistry, global_metrics
from app.observability.schemas import (
    AlertRuleSchema,
    DiagnosticsResponseSchema,
    HealthResponseSchema,
)
from app.observability.tracing import TracerProvider, global_tracer


class ObservabilityService:
    """
    Observability Service.
    Coordinates OpenTelemetry tracing, Prometheus metrics exposition, health checks,
    runtime diagnostics, and alerting.
    """

    def __init__(
        self,
        session: AsyncSession | None = None,
        tracer: TracerProvider | None = None,
        metrics: SystemMetricsRegistry | None = None,
        alert_manager: AlertManager | None = None,
    ) -> None:
        self.tracer = tracer or global_tracer
        self.metrics = metrics or global_metrics
        self.alert_manager = alert_manager or global_alert_manager
        self.health_checker = HealthChecker(session=session)

    async def get_liveness(self) -> HealthResponseSchema:
        """Get instant system liveness status."""
        return await self.health_checker.check_liveness()

    async def get_readiness(self) -> HealthResponseSchema:
        """Get comprehensive readiness status across database, AI, and search."""
        return await self.health_checker.check_readiness()

    def get_prometheus_metrics(self) -> str:
        """Get metrics in standard Prometheus text-based exposition format."""
        return self.metrics.generate_prometheus_format()

    def get_diagnostics(self) -> DiagnosticsResponseSchema:
        """Get runtime diagnostics, version info, and feature flags."""
        return DiagnosticsProvider.get_diagnostics()

    def get_alerts(self) -> list[AlertRuleSchema]:
        """Get configured alert rules and firing status."""
        return self.alert_manager.list_alerts()
