"""Backpressure handling, rate limiting, and slow consumer overflow protection."""

from __future__ import annotations

import time
from dataclasses import dataclass

from app.realtime.exceptions import BackpressureError


@dataclass
class BackpressureConfig:
    """Configurable backpressure threshold limits."""

    max_queue_size: int = 100
    max_rate_per_sec: int = 50
    slow_consumer_timeout_sec: float = 2.0


class BackpressureController:
    """Controls connection message rate limits and outbound queue bounds."""

    def __init__(self, config: BackpressureConfig | None = None) -> None:
        self.config = config or BackpressureConfig()
        self._msg_timestamps: dict[str, list[float]] = {}
        self._dropped_count: int = 0

    def check_rate_limit(self, client_id: str) -> None:
        """Enforce rate limits per client ID."""
        now = time.monotonic()
        history = self._msg_timestamps.get(client_id, [])
        # Retain timestamps within last 1 second
        history = [t for t in history if now - t <= 1.0]

        if len(history) >= self.config.max_rate_per_sec:
            self._dropped_count += 1
            raise BackpressureError(
                f"Client {client_id} exceeded rate limit of {self.config.max_rate_per_sec} msg/s."
            )

        history.append(now)
        self._msg_timestamps[client_id] = history

    def check_queue_overflow(self, current_queue_size: int) -> None:
        """Check if outbound client queue exceeds max allowed queue size."""
        if current_queue_size >= self.config.max_queue_size:
            self._dropped_count += 1
            raise BackpressureError(
                f"Outbound queue overflow: current size {current_queue_size} >= max {self.config.max_queue_size}"
            )

    @property
    def total_dropped(self) -> int:
        return self._dropped_count
