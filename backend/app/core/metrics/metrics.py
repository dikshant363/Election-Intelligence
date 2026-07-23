"""Abstract metrics and telemetry contracts."""

from abc import ABC, abstractmethod
from typing import Any


class Counter(ABC):
    """Abstract counter metric interface."""

    @abstractmethod
    def inc(self, amount: float = 1.0) -> None:
        """Increment counter by specified amount."""
        pass


class Gauge(ABC):
    """Abstract gauge metric interface."""

    @abstractmethod
    def set(self, value: float) -> None:
        """Set gauge to exact value."""
        pass

    @abstractmethod
    def inc(self, amount: float = 1.0) -> None:
        """Increment gauge by specified amount."""
        pass

    @abstractmethod
    def dec(self, amount: float = 1.0) -> None:
        """Decrement gauge by specified amount."""
        pass


class Histogram(ABC):
    """Abstract histogram metric interface."""

    @abstractmethod
    def observe(self, value: float) -> None:
        """Record an observed value in the histogram."""
        pass


class Tracer(ABC):
    """Abstract distributed tracing interface."""

    @abstractmethod
    def start_span(self, name: str) -> Any:
        """Start a new telemetry trace span."""
        pass


class MetricsRegistry(ABC):
    """Abstract metrics registry interface for retrieving metric instruments."""

    @abstractmethod
    def counter(self, name: str, description: str = "") -> Counter:
        """Get or create a Counter metric instrument."""
        pass

    @abstractmethod
    def gauge(self, name: str, description: str = "") -> Gauge:
        """Get or create a Gauge metric instrument."""
        pass

    @abstractmethod
    def histogram(self, name: str, description: str = "") -> Histogram:
        """Get or create a Histogram metric instrument."""
        pass
