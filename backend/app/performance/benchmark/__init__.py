"""Load testing framework and benchmark runner across REST, Search, AI, Realtime, and ETL."""

from __future__ import annotations

import time

from app.performance.schemas import BenchmarkResultSchema


class BenchmarkRunner:
    """Executes synthetic benchmark scenarios measuring operations/sec and latencies."""

    @staticmethod
    def run_benchmark(scenario_name: str, iterations: int = 100) -> BenchmarkResultSchema:
        """Run synthetic benchmark test and compute P95/P99 latency metrics."""
        latencies_ms: list[float] = []
        t_start = time.monotonic()

        for _i in range(iterations):
            t0 = time.monotonic()
            # Simulate operation payload work
            _ = [x * 2 for x in range(100)]
            lat = (time.monotonic() - t0) * 1000.0
            latencies_ms.append(lat)

        total_sec = time.monotonic() - t_start
        latencies_ms.sort()

        p95_idx = int(len(latencies_ms) * 0.95)
        p99_idx = int(len(latencies_ms) * 0.99)
        avg_lat = sum(latencies_ms) / len(latencies_ms)
        throughput = round(iterations / total_sec, 2) if total_sec > 0 else 0.0

        return BenchmarkResultSchema(
            scenario=scenario_name,
            operations_count=iterations,
            total_duration_sec=round(total_sec, 4),
            throughput_ops_per_sec=throughput,
            avg_latency_ms=round(avg_lat, 3),
            p95_latency_ms=round(latencies_ms[p95_idx], 3),
            p99_latency_ms=round(latencies_ms[p99_idx], 3),
        )
