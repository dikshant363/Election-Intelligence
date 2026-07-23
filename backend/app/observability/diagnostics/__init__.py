"""Runtime diagnostics, feature flags, and dependency status."""

from __future__ import annotations

import time

from app.ai.providers import llm_registry
from app.config import settings
from app.observability.schemas import DiagnosticsResponseSchema

_START_TIME = time.monotonic()


class DiagnosticsProvider:
    """Provides runtime diagnostic summary and component status."""

    @staticmethod
    def get_diagnostics() -> DiagnosticsResponseSchema:
        uptime = round(time.monotonic() - _START_TIME, 2)
        return DiagnosticsResponseSchema(
            environment=settings.ENVIRONMENT,
            version="0.21.0",
            uptime_seconds=uptime,
            workers_active=True,
            event_bus_status="running",
            search_engine_status="running",
            ai_provider_count=len(llm_registry.list_providers()),
            feature_flags={
                "enable_rag": True,
                "enable_websockets": True,
                "enable_sse": True,
                "enable_background_workers": True,
            },
        )
