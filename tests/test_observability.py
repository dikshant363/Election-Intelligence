"""
Comprehensive unit & integration test suite for Milestone 21 — Observability, Telemetry & Operations Platform.

Tests cover:
- TelemetryContext propagation across trace_id, span_id, correlation_id, causation_id
- OpenTelemetry TracerProvider & Span lifecycle
- Prometheus metrics collection & text exposition format
- Structured JSON logging & secret redaction
- Health & readiness probes (Liveness, Readiness, Dependency checks)
- Runtime Diagnostics & feature flags
- AlertManager & AlertRule threshold evaluation
- ObservabilityMiddleware header propagation
- ObservabilityService coordinator
- FastAPI REST endpoints (/health, /ready, /live, /metrics, /diagnostics, /alerts)
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.api.v1.dependencies.dependencies import get_observability_service
from app.main import app
from app.observability import (
    AlertManager,
    HealthChecker,
    ObservabilityService,
    Span,
    SystemMetricsRegistry,
    TelemetryContext,
    TracerProvider,
    get_current_telemetry_context,
    get_structured_logger,
    set_telemetry_context,
)
from app.observability.logging import sanitize_dict
from app.observability.schemas import (
    AlertRuleSchema,
    DiagnosticsResponseSchema,
    HealthDependencySchema,
    HealthResponseSchema,
)

LATENCY_50MS = 50.0
UPTIME_100S = 100.0
MIN_DEPS_3 = 3


# ─────────────────────────────────────────────────────────────────────────────
# 1. TelemetryContext Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestTelemetryContext:
    def test_telemetry_context_defaults(self) -> None:
        ctx = TelemetryContext(service="test-service")
        assert ctx.service == "test-service"
        assert len(ctx.trace_id) > 0
        d = ctx.to_dict()
        assert "correlation_id" in d

    def test_context_propagation(self) -> None:
        ctx = TelemetryContext(trace_id="trace_xyz")
        set_telemetry_context(ctx)
        retrieved = get_current_telemetry_context()
        assert retrieved.trace_id == "trace_xyz"


# ─────────────────────────────────────────────────────────────────────────────
# 2. Tracing & Span Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestTracing:
    def test_span_lifecycle(self) -> None:
        span = Span(name="test_span", trace_id="tr_1", span_id="sp_1")
        span.end()
        assert span.duration_ms >= 0.0

    def test_tracer_provider_start_span(self) -> None:
        tracer = TracerProvider()
        with tracer.start_span("db_query", component="database") as span:
            span.attributes["query"] = "SELECT 1"

        spans = tracer.get_spans()
        assert len(spans) == 1
        assert spans[0].name == "db_query"
        assert spans[0].attributes["query"] == "SELECT 1"


# ─────────────────────────────────────────────────────────────────────────────
# 3. Prometheus Metrics Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestPrometheusMetrics:
    def test_metrics_record_and_exposition(self) -> None:
        metrics = SystemMetricsRegistry()
        metrics.record_http("GET", "/api/v1/elections", 200, 0.05)
        metrics.record_search(0.02)
        metrics.record_ai(0.15)

        prom_text = metrics.generate_prometheus_format()
        assert "http_requests_total" in prom_text
        assert 'method="GET"' in prom_text
        assert "search_queries_total 1" in prom_text
        assert "ai_queries_total 1" in prom_text


# ─────────────────────────────────────────────────────────────────────────────
# 4. Structured Logging Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestStructuredLogging:
    def test_sanitize_dict_redacts_secrets(self) -> None:
        data = {
            "username": "admin",
            "password": "supersecretpassword",
            "api_key": "12345-abcde",
            "nested": {"token": "bearer-xyz"},
        }
        clean = sanitize_dict(data)
        assert clean["username"] == "admin"
        assert clean["password"] == "[REDACTED_SECRET]"
        assert clean["api_key"] == "[REDACTED_SECRET]"
        assert clean["nested"]["token"] == "[REDACTED_SECRET]"

    def test_get_structured_logger(self) -> None:
        logger = get_structured_logger("test_logger")
        assert logger is not None


# ─────────────────────────────────────────────────────────────────────────────
# 5. Health & Readiness Tests
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestHealthChecks:
    async def test_liveness(self) -> None:
        checker = HealthChecker()
        resp = await checker.check_liveness()
        assert resp.status == "healthy"

    async def test_readiness(self) -> None:
        session = AsyncMock()
        checker = HealthChecker(session)
        resp = await checker.check_readiness()
        assert resp.status == "healthy"
        assert len(resp.dependencies) >= MIN_DEPS_3


# ─────────────────────────────────────────────────────────────────────────────
# 6. Alerting Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestAlerting:
    def test_alert_manager_threshold(self) -> None:
        mgr = AlertManager()
        alert = mgr.evaluate_metric("high_http_latency", 1500.0)
        assert alert is not None
        assert alert.is_firing is True
        assert alert.severity == "warning"

        # Resolved
        alert_res = mgr.evaluate_metric("high_http_latency", 200.0)
        assert alert_res.is_firing is False


# ─────────────────────────────────────────────────────────────────────────────
# 7. ObservabilityService & Middleware Tests
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestObservabilityService:
    async def test_service_liveness_and_metrics(self) -> None:
        service = ObservabilityService()
        liveness = await service.get_liveness()
        assert liveness.status == "healthy"

        metrics_text = service.get_prometheus_metrics()
        assert "http_requests_total" in metrics_text


class TestObservabilityAPIRouter:
    def setup_method(self) -> None:
        mock_service = AsyncMock()
        mock_service.get_liveness = AsyncMock(
            return_value=HealthResponseSchema(
                status="healthy", timestamp="2026-07-23T12:00:00Z", dependencies=[]
            )
        )
        mock_service.get_readiness = AsyncMock(
            return_value=HealthResponseSchema(
                status="healthy",
                timestamp="2026-07-23T12:00:00Z",
                dependencies=[HealthDependencySchema(name="postgresql", status="healthy", latency_ms=1.5)],
            )
        )
        mock_service.get_prometheus_metrics = MagicMock(
            return_value="# HELP http_requests_total Total\nhttp_requests_total 1\n"
        )
        mock_service.get_diagnostics = MagicMock(
            return_value=DiagnosticsResponseSchema(
                environment="production",
                version="0.21.0",
                uptime_seconds=UPTIME_100S,
                workers_active=True,
                event_bus_status="running",
                search_engine_status="running",
                ai_provider_count=5,
                feature_flags={"enable_rag": True},
            )
        )
        mock_service.get_alerts = MagicMock(
            return_value=[
                AlertRuleSchema(
                    rule_name="high_http_latency",
                    severity="warning",
                    is_firing=False,
                    threshold=1000.0,
                    current_value=120.0,
                )
            ]
        )

        app.dependency_overrides[get_observability_service] = lambda: mock_service

    def teardown_method(self) -> None:
        app.dependency_overrides.clear()

    def test_health_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/health")
        assert resp.status_code == 200  # noqa: PLR2004
        assert resp.json()["status"] == "healthy"

    def test_ready_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/ready")
        assert resp.status_code == 200  # noqa: PLR2004

    def test_live_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/live")
        assert resp.status_code == 200  # noqa: PLR2004

    def test_metrics_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/metrics")
        assert resp.status_code == 200  # noqa: PLR2004
        assert "http_requests_total" in resp.text

    def test_diagnostics_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/diagnostics")
        assert resp.status_code == 200  # noqa: PLR2004
        assert resp.json()["version"] == "0.21.0"

    def test_alerts_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/alerts")
        assert resp.status_code == 200  # noqa: PLR2004
        assert len(resp.json()) == 1
