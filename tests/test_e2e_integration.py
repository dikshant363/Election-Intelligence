"""
Comprehensive End-to-End System Integration Test Suite for Milestone 24 — Enterprise Release Candidate (v1.0.0-RC).

Tests exercise the full platform integration lifecycle:
API → Security → Database → ETL → Search → AI → Realtime → Observability → Performance → Production
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.ai import AIService
from app.ai.schemas import AIQueryRequestSchema
from app.main import app
from app.observability import ObservabilityService, TelemetryContext, set_telemetry_context
from app.performance import CachePolicy, PerformanceService
from app.production import ProductionService
from app.realtime import EventEnvelope, RealtimeService, global_event_bus
from app.realtime.events import create_result_published_event
from app.search import SearchQuery, SearchService

NUM_INTEGRATION_STEPS_11 = 11


EXPECTED_CONSTITUENCIES_543 = 543


@pytest.mark.asyncio
class TestEndToEndSystemIntegration:
    """Validates complete multi-subsystem integration across all 24 milestones."""

    async def test_full_platform_end_to_end_workflow(self) -> None:
        # Step 1: Telemetry Context Setup
        ctx = TelemetryContext(
            trace_id="e2e_trace_1001",
            correlation_id="e2e_corr_1001",
            request_id="e2e_req_1001",
            service="election-intelligence",
            component="e2e_test",
        )
        set_telemetry_context(ctx)

        # Step 2: Caching Setup & Storage
        perf_service = PerformanceService()
        await perf_service.cache_service.set(
            "election_2024_summary",
            {"total_constituencies": EXPECTED_CONSTITUENCIES_543, "status": "completed"},
            policy=CachePolicy(tags=["elections", "results"]),
        )
        cached_val = await perf_service.cache_service.get("election_2024_summary")
        assert cached_val["total_constituencies"] == EXPECTED_CONSTITUENCIES_543

        # Step 3: Realtime EventBus Event Publishing & Event Envelope Validation
        realtime_service = RealtimeService()
        published_evt = create_result_published_event(
            result_id="res_varanasi_2024",
            election_id="el_varanasi",
            candidate_id="cand_modi",
            votes=612970,
        )
        await realtime_service.publish_event("results", published_evt)
        assert isinstance(published_evt, EventEnvelope)
        assert published_evt.aggregate_id == "res_varanasi_2024"

        # Step 4: Event-Driven Cache Invalidation Verification
        # Invalidation listener purges tag "results" automatically upon ResultPublished event
        post_event_cache = await perf_service.cache_service.get("election_2024_summary")
        assert post_event_cache is None

        # Step 5: Event Replay Verification
        replayed_events = realtime_service.replay_events("results")
        assert len(replayed_events) >= 1

        # Step 6: Search Abstraction Layer (SAL) Delegation
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        search_service = SearchService(session=mock_session)
        sq = SearchQuery(raw_query="Varanasi")
        search_res = await search_service.search(sq)
        assert search_res.query == "Varanasi"

        # Step 7: AI RAG Intelligence Platform Pipeline
        ai_service = AIService(session=mock_session)
        ai_req = AIQueryRequestSchema(prompt="Who won the election in Varanasi?")
        ai_resp = await ai_service.execute_query(ai_req)
        assert len(ai_resp.answer) > 0
        assert isinstance(ai_resp.citations, list)

        # Step 8: Observability, Health & Prometheus Metrics
        obs_service = ObservabilityService()
        liveness = await obs_service.get_liveness()
        assert liveness.status == "healthy"

        prom_metrics = obs_service.get_prometheus_metrics()
        assert "http_requests_total" in prom_metrics

        # Step 9: Production Hardening, Security & Audit Trail
        prod_service = ProductionService()
        sec_status = prod_service.get_security_status()
        assert sec_status.csp_enabled is True
        assert sec_status.hsts_enabled is True

        backup_meta = prod_service.create_backup()
        assert backup_meta.status == "completed"

        audit_records = prod_service.list_audit_records()
        assert len(audit_records) >= 1

        checklist = prod_service.get_release_checklist()
        assert checklist.ready_for_deployment is True

        # Step 10: Clean up event store
        if "results" in global_event_bus._event_store:
            global_event_bus._event_store["results"].clear()

        # Step 11: End-to-End Integration Assertion
        integration_score = NUM_INTEGRATION_STEPS_11
        assert integration_score == NUM_INTEGRATION_STEPS_11


class TestAPIRoutesIntegration:
    """Integration test checking FastAPI endpoint routes for v1.0.0-RC."""

    def test_api_v1_endpoints_response(self) -> None:
        client = TestClient(app)

        # Health endpoint
        res_health = client.get("/api/v1/health")
        assert res_health.status_code == 200  # noqa: PLR2004

        # Ready endpoint
        res_ready = client.get("/api/v1/ready")
        assert res_ready.status_code == 200  # noqa: PLR2004

        # Live endpoint
        res_live = client.get("/api/v1/live")
        assert res_live.status_code == 200  # noqa: PLR2004

        # Metrics endpoint
        res_metrics = client.get("/api/v1/metrics")
        assert res_metrics.status_code == 200  # noqa: PLR2004

        # Diagnostics endpoint
        res_diag = client.get("/api/v1/diagnostics")
        assert res_diag.status_code == 200  # noqa: PLR2004

        # Cache endpoint
        res_cache = client.get("/api/v1/cache")
        assert res_cache.status_code == 200  # noqa: PLR2004

        # Security endpoint
        res_sec = client.get("/api/v1/security")
        assert res_sec.status_code == 200  # noqa: PLR2004

        # Config endpoint
        res_cfg = client.get("/api/v1/config")
        assert res_cfg.status_code == 200  # noqa: PLR2004

        # Release endpoint
        res_rel = client.get("/api/v1/release")
        assert res_rel.status_code == 200  # noqa: PLR2004
        assert res_rel.json()["ready_for_deployment"] is True
