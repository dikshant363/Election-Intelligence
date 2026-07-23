"""Unit tests for metrics and telemetry interfaces."""

from typing import Any

import pytest
from app.core.metrics import Counter, Gauge, Histogram, MetricsRegistry, Tracer


class DummyCounter(Counter):
    def __init__(self) -> None:
        self.val = 0.0

    def inc(self, amount: float = 1.0) -> None:
        self.val += amount


class DummyGauge(Gauge):
    def __init__(self) -> None:
        self.val = 0.0

    def set(self, value: float) -> None:
        self.val = value

    def inc(self, amount: float = 1.0) -> None:
        self.val += amount

    def dec(self, amount: float = 1.0) -> None:
        self.val -= amount


class DummyHistogram(Histogram):
    def __init__(self) -> None:
        self.observations: list[float] = []

    def observe(self, value: float) -> None:
        self.observations.append(value)


class DummyTracer(Tracer):
    def start_span(self, name: str) -> Any:
        return {"span_name": name}


class DummyMetricsRegistry(MetricsRegistry):
    def counter(self, name: str, description: str = "") -> Counter:
        return DummyCounter()

    def gauge(self, name: str, description: str = "") -> Gauge:
        return DummyGauge()

    def histogram(self, name: str, description: str = "") -> Histogram:
        return DummyHistogram()


def test_metrics_contracts_execution() -> None:
    """Verify counter, gauge, histogram, tracer, and registry interfaces."""
    registry = DummyMetricsRegistry()

    c = registry.counter("test_counter")
    c.inc(5.0)
    assert getattr(c, "val") == 5.0

    g = registry.gauge("test_gauge")
    g.set(10.0)
    g.inc(2.0)
    g.dec(1.0)
    assert getattr(g, "val") == 11.0

    h = registry.histogram("test_histogram")
    h.observe(42.0)
    assert getattr(h, "observations") == [42.0]

    t = DummyTracer()
    span = t.start_span("test_span")
    assert span["span_name"] == "test_span"
