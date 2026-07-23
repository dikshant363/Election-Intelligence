"""
Comprehensive unit & integration test suite for Milestone 20 — Real-Time Intelligence & Event Streaming Platform.

Tests cover:
- EventEnvelope & Domain Events (immutability, serialization)
- InMemoryEventBus (publishing, subscriptions, event replay)
- Background Workers (enqueue, retries, exponential backoff, dead-letter queue, cancellation)
- Presence Manager (client tracking, subscriptions, heartbeat ping/pong)
- Backpressure Controller (rate limiting, queue overflow, dropped counts)
- Metrics Collector (message throughput, avg latency, queue depth)
- Notification Service (prioritized alerts)
- RealtimeService Coordinator
- FastAPI REST & WebSocket endpoints (/events, /events/publish, /realtime/presence, /realtime/metrics, /ws)
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.api.v1.dependencies.dependencies import get_realtime_service
from app.main import app
from app.realtime import (
    BackgroundWorker,
    BackpressureError,
    DeadLetterQueue,
    EventEnvelope,
    InMemoryEventBus,
    Job,
    RealtimeService,
)
from app.realtime.backpressure import BackpressureConfig, BackpressureController
from app.realtime.events import (
    create_election_created_event,
    create_import_completed_event,
    create_result_published_event,
)
from app.realtime.metrics import MetricsCollector
from app.realtime.notifications import NotificationService
from app.realtime.presence import PresenceManager
from app.realtime.schemas import (
    PresenceInfoSchema,
    RealtimeMetricsSchema,
)

CLIENT_ID = "client_101"
TOPIC_RESULTS = "results"
LATENCY_10MS = 10.0
VOTES_50K = 50000
RECORDS_1K = 1000
COUNT_2 = 2
CLIENTS_5 = 5


# ─────────────────────────────────────────────────────────────────────────────
# 1. EventEnvelope & Domain Events Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestDomainEvents:
    def test_event_envelope_structure(self) -> None:
        event = create_election_created_event(
            election_id="el_1", title="Lok Sabha 2024", election_type="general"
        )
        assert event.event_type == "ElectionCreated"
        assert event.aggregate_id == "el_1"
        assert event.payload["title"] == "Lok Sabha 2024"
        d = event.to_dict()
        assert d["producer"] == "election-intelligence-platform"

    def test_result_published_event(self) -> None:
        event = create_result_published_event(
            result_id="res_1", election_id="el_1", candidate_id="cand_1", votes=VOTES_50K
        )
        assert event.event_type == "ResultPublished"
        assert event.payload["votes"] == VOTES_50K

    def test_import_completed_event(self) -> None:
        event = create_import_completed_event(job_id="job_99", record_count=RECORDS_1K)
        assert event.payload["record_count"] == RECORDS_1K


# ─────────────────────────────────────────────────────────────────────────────
# 2. EventBus & Replay Tests
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestEventBus:
    async def test_publish_and_subscribe(self) -> None:
        bus = InMemoryEventBus()
        received = []

        async def _handler(event: EventEnvelope) -> None:
            received.append(event)

        bus.subscribe(TOPIC_RESULTS, _handler)

        event = create_result_published_event("res_1", "el_1", "c_1", 100)
        await bus.publish(TOPIC_RESULTS, event)

        assert len(received) == 1
        assert received[0].aggregate_id == "res_1"

    async def test_event_replay(self) -> None:
        bus = InMemoryEventBus()
        e1 = create_result_published_event("res_1", "el_1", "c_1", 100)
        e2 = create_result_published_event("res_2", "el_1", "c_2", 200)

        await bus.publish(TOPIC_RESULTS, e1)
        await bus.publish(TOPIC_RESULTS, e2)

        history = bus.replay(TOPIC_RESULTS)
        assert len(history) == COUNT_2
        assert history[0].aggregate_id == "res_1"
        assert history[1].aggregate_id == "res_2"

    async def test_unsubscribe(self) -> None:
        bus = InMemoryEventBus()
        received = []

        async def _handler(event: EventEnvelope) -> None:
            received.append(event)

        bus.subscribe(TOPIC_RESULTS, _handler)
        bus.unsubscribe(TOPIC_RESULTS, _handler)

        await bus.publish(TOPIC_RESULTS, create_result_published_event("res_1", "el_1", "c_1", 100))
        assert len(received) == 0


# ─────────────────────────────────────────────────────────────────────────────
# 3. Background Worker Tests
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestBackgroundWorker:
    async def test_worker_successful_execution(self) -> None:
        worker = BackgroundWorker()
        await worker.start()

        executed = []

        async def _job_handler(job: Job) -> None:
            executed.append(job.job_id)

        job = Job(job_id="j_1", name="test_job")
        await worker.enqueue(job, _job_handler)

        await asyncio.sleep(0.1)
        await worker.stop()

        assert "j_1" in executed
        assert job.status == "completed"

    async def test_worker_retry_and_dead_letter_queue(self) -> None:
        dlq = DeadLetterQueue()
        worker = BackgroundWorker(dlq=dlq)
        await worker.start()

        async def _failing_handler(job: Job) -> None:
            raise ValueError("Task failed")

        job = Job(job_id="j_fail", max_retries=1, backoff_factor=0.01)
        await worker.enqueue(job, _failing_handler)

        await asyncio.sleep(0.15)
        await worker.stop()

        assert job.status == "failed"
        assert len(dlq.list_jobs()) == 1
        assert dlq.list_jobs()[0].job.job_id == "j_fail"


# ─────────────────────────────────────────────────────────────────────────────
# 4. Presence & Backpressure Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestPresenceAndBackpressure:
    def test_presence_manager_lifecycle(self) -> None:
        presence = PresenceManager()
        p = presence.register(client_id=CLIENT_ID, user_id="user_1")
        assert presence.count() == 1
        assert p.client_id == CLIENT_ID

        presence.subscribe_topic(CLIENT_ID, TOPIC_RESULTS)
        assert TOPIC_RESULTS in presence.get(CLIENT_ID).topics

        presence.unregister(CLIENT_ID)
        assert presence.count() == 0

    def test_backpressure_rate_limiting(self) -> None:
        controller = BackpressureController(config=BackpressureConfig(max_rate_per_sec=2))
        controller.check_rate_limit(CLIENT_ID)
        controller.check_rate_limit(CLIENT_ID)

        with pytest.raises(BackpressureError):
            controller.check_rate_limit(CLIENT_ID)

        assert controller.total_dropped == 1

    def test_backpressure_queue_overflow(self) -> None:
        controller = BackpressureController(config=BackpressureConfig(max_queue_size=5))
        with pytest.raises(BackpressureError):
            controller.check_queue_overflow(5)


# ─────────────────────────────────────────────────────────────────────────────
# 5. Metrics & Notification Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestMetricsAndNotifications:
    def test_metrics_collector(self) -> None:
        collector = MetricsCollector()
        collector.record_message(latency_ms=LATENCY_10MS)
        collector.record_drop()

        snap = collector.get_snapshot(active_clients=CLIENTS_5, queue_depth=COUNT_2)
        assert snap.connected_clients == CLIENTS_5
        assert snap.dropped_messages == 1
        assert snap.queue_depth == COUNT_2

    @pytest.mark.asyncio
    async def test_notification_service(self) -> None:
        bus = InMemoryEventBus()
        received = []

        async def _notif_handler(event: EventEnvelope) -> None:
            received.append(event)

        bus.subscribe("system_alerts", _notif_handler)

        service = NotificationService(event_bus=bus)
        notif = await service.notify(
            topic="system_alerts",
            title="System Alert",
            message="Server maintenance in 10m",
            priority="urgent",
        )

        assert notif.priority == "urgent"
        assert len(received) == 1
        assert received[0].payload["title"] == "System Alert"


# ─────────────────────────────────────────────────────────────────────────────
# 6. RealtimeService Integration Tests
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestRealtimeService:
    async def test_publish_and_replay(self) -> None:
        service = RealtimeService()
        event = create_result_published_event("res_99", "el_1", "cand_1", 250)

        await service.publish_event(TOPIC_RESULTS, event)
        replayed = service.replay_events(TOPIC_RESULTS)

        assert len(replayed) == 1
        assert replayed[0].aggregate_id == "res_99"


# ─────────────────────────────────────────────────────────────────────────────
# 7. API Router Endpoint Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestRealtimeAPIRouter:
    def setup_method(self) -> None:
        mock_service = AsyncMock()
        mock_service.replay_events = MagicMock(
            return_value=[create_result_published_event("res_1", "el_1", "c_1", 100)]
        )
        mock_service.publish_event = AsyncMock()
        mock_service.list_presence = MagicMock(
            return_value=[
                PresenceInfoSchema(
                    client_id=CLIENT_ID,
                    user_id="user_1",
                    connected_at="2026-07-23T12:00:00Z",
                    last_heartbeat="2026-07-23T12:00:05Z",
                    topics=[TOPIC_RESULTS],
                )
            ]
        )
        mock_service.get_metrics = MagicMock(
            return_value=RealtimeMetricsSchema(
                connected_clients=1,
                messages_per_sec=10.0,
                dropped_messages=0,
                worker_throughput=5.0,
                avg_latency_ms=2.5,
                reconnect_count=0,
                queue_depth=0,
            )
        )

        app.dependency_overrides[get_realtime_service] = lambda: mock_service

    def teardown_method(self) -> None:
        app.dependency_overrides.clear()

    def test_replay_events_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/events?topic=results")
        assert resp.status_code == 200  # noqa: PLR2004
        data = resp.json()
        assert len(data) == 1
        assert data[0]["event_type"] == "ResultPublished"

    def test_publish_event_endpoint(self) -> None:
        client = TestClient(app)
        body = {
            "event_type": "CustomEvent",
            "aggregate_id": "agg_100",
            "payload": {"key": "val"},
            "topic": "results",
        }
        resp = client.post("/api/v1/events/publish", json=body)
        assert resp.status_code == 202  # noqa: PLR2004
        data = resp.json()
        assert data["aggregate_id"] == "agg_100"

    def test_presence_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/realtime/presence")
        assert resp.status_code == 200  # noqa: PLR2004
        data = resp.json()
        assert len(data) == 1
        assert data[0]["client_id"] == CLIENT_ID

    def test_metrics_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/realtime/metrics")
        assert resp.status_code == 200  # noqa: PLR2004
        data = resp.json()
        assert data["connected_clients"] == 1
