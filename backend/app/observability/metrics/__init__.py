"""Prometheus metrics collector and text exposition format generator."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class MetricCounter:
    """Counter metric."""

    name: str
    help_text: str
    labels: dict[str, str] = field(default_factory=dict)
    value: float = 0.0


class SystemMetricsRegistry:
    """Registry maintaining system Counters, Gauges, and Histograms."""

    def __init__(self) -> None:
        self.http_requests: dict[str, int] = defaultdict(int)
        self.http_latency_sum: dict[str, float] = defaultdict(float)
        self.search_queries: int = 0
        self.search_latency_sum: float = 0.0
        self.ai_queries: int = 0
        self.ai_latency_sum: float = 0.0
        self.worker_jobs_completed: int = 0
        self.worker_jobs_failed: int = 0
        self.event_count: int = 0

    def record_http(self, method: str, endpoint: str, status_code: int, duration_sec: float) -> None:
        key = f"{method}:{endpoint}:{status_code}"
        self.http_requests[key] += 1
        self.http_latency_sum[key] += duration_sec

    def record_search(self, duration_sec: float) -> None:
        self.search_queries += 1
        self.search_latency_sum += duration_sec

    def record_ai(self, duration_sec: float) -> None:
        self.ai_queries += 1
        self.ai_latency_sum += duration_sec

    def generate_prometheus_format(self) -> str:
        """Generate standard Prometheus text-based exposition format string."""
        lines = [
            "# HELP http_requests_total Total HTTP requests processed.",
            "# TYPE http_requests_total counter",
        ]
        for key, count in self.http_requests.items():
            parts = key.split(":")
            lines.append(
                f'http_requests_total{{method="{parts[0]}",endpoint="{parts[1]}",status="{parts[2]}"}} {count}'
            )

        lines.extend([
            "# HELP search_queries_total Total search queries.",
            "# TYPE search_queries_total counter",
            f"search_queries_total {self.search_queries}",
            "# HELP ai_queries_total Total AI queries.",
            "# TYPE ai_queries_total counter",
            f"ai_queries_total {self.ai_queries}",
            "# HELP worker_jobs_completed_total Total completed worker jobs.",
            "# TYPE worker_jobs_completed_total counter",
            f"worker_jobs_completed_total {self.worker_jobs_completed}",
        ])
        return "\n".join(lines) + "\n"


# Singleton metrics registry
global_metrics = SystemMetricsRegistry()
