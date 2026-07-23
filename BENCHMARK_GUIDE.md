# Performance Benchmarking & Load Testing Guide

## Overview

The `BenchmarkRunner` framework executes synthetic load scenarios across REST APIs, Search, AI, Realtime, and ETL pipelines to measure throughput and latency percentiles.

---

## Executing Benchmarks

Via API endpoint:

```text
GET /api/v1/benchmark?scenario=rest_api&iterations=100
```

Sample JSON response:

```json
{
  "scenario": "rest_api",
  "operations_count": 100,
  "total_duration_sec": 0.0512,
  "throughput_ops_per_sec": 1953.12,
  "avg_latency_ms": 0.51,
  "p95_latency_ms": 0.85,
  "p99_latency_ms": 1.20
}
```

---

## Programmatic Execution

```python
from app.performance.benchmark import BenchmarkRunner

res = BenchmarkRunner.run_benchmark("search_query", iterations=500)
print(f"Throughput: {res.throughput_ops_per_sec} ops/sec, P95: {res.p95_latency_ms}ms")
```
