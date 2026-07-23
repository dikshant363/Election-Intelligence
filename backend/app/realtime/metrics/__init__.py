"""Realtime metrics collector tracking connections, throughput, dropped messages, and latency."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from app.realtime.schemas import RealtimeMetricsSchema


@dataclass
class MetricsCollector:
    """Collects real-time system performance statistics."""

    connected_clients: int = 0
    total_messages: int = 0
    dropped_messages: int = 0
    worker_jobs_completed: int = 0
    reconnect_count: int = 0
    total_latency_ms: float = 0.0
    start_time: float = field(default_factory=time.monotonic)

    def record_message(self, latency_ms: float = 0.0) -> None:
        self.total_messages += 1
        self.total_latency_ms += latency_ms

    def record_drop(self) -> None:
        self.dropped_messages += 1

    def record_reconnect(self) -> None:
        self.reconnect_count += 1

    def get_snapshot(self, active_clients: int, queue_depth: int = 0) -> RealtimeMetricsSchema:
        elapsed = max(1.0, time.monotonic() - self.start_time)
        msg_rate = round(self.total_messages / elapsed, 2)
        worker_tp = round(self.worker_jobs_completed / elapsed, 2)
        avg_lat = round(self.total_latency_ms / max(1, self.total_messages), 2)

        return RealtimeMetricsSchema(
            connected_clients=active_clients,
            messages_per_sec=msg_rate,
            dropped_messages=self.dropped_messages,
            worker_throughput=worker_tp,
            avg_latency_ms=avg_lat,
            reconnect_count=self.reconnect_count,
            queue_depth=queue_depth,
        )
