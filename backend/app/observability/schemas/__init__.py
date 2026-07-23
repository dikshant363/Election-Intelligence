"""Pydantic v2 schemas for Observability & Operations APIs."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TelemetryContextSchema(BaseModel):
    """Standardized Telemetry Context specification."""

    model_config = ConfigDict(frozen=True)

    trace_id: str
    span_id: str
    correlation_id: str
    causation_id: str
    request_id: str
    user_id: str | None = None
    session_id: str | None = None
    service: str = "election-intelligence"
    component: str = "api"
    environment: str = "production"
    metadata: dict[str, Any] = Field(default_factory=dict)


class HealthDependencySchema(BaseModel):
    """Dependency component health status."""

    model_config = ConfigDict(frozen=True)

    name: str
    status: str = Field(..., description="healthy, degraded, unhealthy")
    latency_ms: float = 0.0
    details: dict[str, Any] = Field(default_factory=dict)


class HealthResponseSchema(BaseModel):
    """Comprehensive health check status response (backward compatible)."""

    model_config = ConfigDict(frozen=True)

    status: str = Field(..., description="healthy, degraded, unhealthy")
    version: str = "v0.21.0"
    timestamp: str
    database: str = "connected"
    request_id: str | None = None
    dependencies: list[HealthDependencySchema] = Field(default_factory=list)


class DiagnosticsResponseSchema(BaseModel):
    """System runtime diagnostics & feature status."""

    model_config = ConfigDict(frozen=True)

    environment: str
    version: str
    uptime_seconds: float
    workers_active: bool
    event_bus_status: str
    search_engine_status: str
    ai_provider_count: int
    feature_flags: dict[str, bool]


class AlertRuleSchema(BaseModel):
    """Alert definition and firing status."""

    model_config = ConfigDict(frozen=True)

    rule_name: str
    severity: str = Field(default="warning", description="info, warning, critical")
    is_firing: bool
    threshold: float
    current_value: float
    triggered_at: str | None = None
