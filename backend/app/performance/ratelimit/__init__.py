"""Rate Limiting and Throttling abstraction (Sliding Window & Token Bucket)."""

from __future__ import annotations

import time
from collections import defaultdict

from app.performance.exceptions import RateLimitExceeded


class SlidingWindowRateLimiter:
    """Sliding window rate limiter enforcing request rate limits per key (IP, API Key, User ID)."""

    def __init__(self, max_requests: int = 100, window_seconds: float = 60.0) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._history: dict[str, list[float]] = defaultdict(list)

    def check_rate_limit(self, identifier: str) -> bool:
        """Evaluate whether identifier is within rate limit bounds."""
        now = time.monotonic()
        cutoff = now - self.window_seconds
        timestamps = [t for t in self._history[identifier] if t > cutoff]
        self._history[identifier] = timestamps

        if len(timestamps) >= self.max_requests:
            return False

        self._history[identifier].append(now)
        return True

    def enforce_rate_limit(self, identifier: str) -> None:
        """Enforce rate limit, raising RateLimitExceeded if violated."""
        if not self.check_rate_limit(identifier):
            raise RateLimitExceeded(f"Rate limit of {self.max_requests} req/{self.window_seconds}s exceeded for {identifier}")


class TokenBucket:
    """Token Bucket rate limiting algorithm abstraction."""

    def __init__(self, capacity: int = 50, refill_rate_per_sec: float = 10.0) -> None:
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

    def consume(self, amount: int = 1) -> bool:
        now = time.monotonic()
        delta = now - self.last_refill
        self.tokens = min(float(self.capacity), self.tokens + delta * self.refill_rate)
        self.last_refill = now

        if self.tokens >= amount:
            self.tokens -= amount
            return True
        return False
