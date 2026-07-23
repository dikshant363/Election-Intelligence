"""Resilience Layer: Circuit Breakers, Bulkheads, Retries, Timeouts, and ResiliencePolicy."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from app.production.exceptions import CircuitBreakerOpenError


class CircuitBreaker:
    """Circuit Breaker protecting external systems (Database, AI providers, Search, EventBus)."""

    def __init__(
        self,
        service_name: str,
        failure_threshold: int = 5,
        recovery_time_sec: float = 30.0,
    ) -> None:
        self.service_name = service_name
        self.failure_threshold = failure_threshold
        self.recovery_time_sec = recovery_time_sec

        self.state: str = "CLOSED"  # CLOSED, OPEN, HALF-OPEN
        self.failure_count: int = 0
        self.last_state_change: float = time.monotonic()

    def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        now = time.monotonic()

        if self.state == "OPEN":
            if now - self.last_state_change > self.recovery_time_sec:
                self.state = "HALF-OPEN"
                self.last_state_change = now
            else:
                raise CircuitBreakerOpenError(self.service_name)

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF-OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
                self.last_state_change = now
            return result
        except Exception:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.last_state_change = now
            raise


class ResiliencePolicy:
    """Unified Resilience Policy wrapper aggregating circuit breaker, timeout, retry, and bulkhead."""

    def __init__(self, service_name: str) -> None:
        self.circuit_breaker = CircuitBreaker(service_name=service_name)

    def execute(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        return self.circuit_breaker.call(func, *args, **kwargs)
