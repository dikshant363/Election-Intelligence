"""Health check service for liveness, readiness, and dependency diagnostics."""

from __future__ import annotations

import time
from datetime import UTC, datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.providers import llm_registry
from app.observability.schemas import HealthDependencySchema, HealthResponseSchema
from app.observability.telemetry import get_current_telemetry_context


class HealthChecker:
    """Evaluates liveness, readiness, and dependency health status."""

    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session

    async def check_liveness(self) -> HealthResponseSchema:
        """Liveness check returning instant operational status."""
        ctx = get_current_telemetry_context()
        return HealthResponseSchema(
            status="healthy",
            timestamp=datetime.now(UTC).isoformat(),
            database="connected",
            request_id=ctx.request_id,
            dependencies=[],
        )

    async def check_readiness(self) -> HealthResponseSchema:
        """Readiness check evaluating all dependency subsystems."""
        deps: list[HealthDependencySchema] = []
        ctx = get_current_telemetry_context()

        # 1. Database Check
        db_status = "connected"
        t0 = time.monotonic()
        if self._session:
            try:
                await self._session.execute(text("SELECT 1"))
            except Exception as err:  # noqa: BLE001
                db_status = "disconnected"
                deps.append(
                    HealthDependencySchema(
                        name="postgresql",
                        status="unhealthy",
                        latency_ms=round((time.monotonic() - t0) * 1000.0, 2),
                        details={"error": str(err)},
                    )
                )
        if db_status == "connected":
            deps.append(
                HealthDependencySchema(
                    name="postgresql",
                    status="healthy",
                    latency_ms=round((time.monotonic() - t0) * 1000.0, 2),
                )
            )

        # 2. EventBus Check
        deps.append(
            HealthDependencySchema(
                name="event_bus",
                status="healthy",
                details={"provider": "InMemoryEventBus"},
            )
        )

        # 3. AI Providers Check
        providers = llm_registry.list_providers()
        deps.append(
            HealthDependencySchema(
                name="ai_providers",
                status="healthy" if providers else "degraded",
                details={"available_providers": providers},
            )
        )

        overall_status = (
            "unhealthy"
            if any(d.status == "unhealthy" for d in deps)
            else ("degraded" if any(d.status == "degraded" for d in deps) else "healthy")
        )

        return HealthResponseSchema(
            status=overall_status,
            timestamp=datetime.now(UTC).isoformat(),
            database=db_status,
            request_id=ctx.request_id,
            dependencies=deps,
        )
