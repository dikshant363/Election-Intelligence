# Prometheus Metrics & Exposition Guide

## Overview

The platform exposes metrics in standard Prometheus text-based exposition format at `GET /api/v1/metrics`.

---

## Exposed Metric Series

```text
# HELP http_requests_total Total HTTP requests processed.
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/api/v1/elections",status="200"} 42

# HELP search_queries_total Total search queries.
# TYPE search_queries_total counter
search_queries_total 128

# HELP ai_queries_total Total AI queries.
# TYPE ai_queries_total counter
ai_queries_total 54

# HELP worker_jobs_completed_total Total completed worker jobs.
# TYPE worker_jobs_completed_total counter
worker_jobs_completed_total 15
```

---

## Grafana & Prometheus Scraping Configuration

```yaml
scrape_configs:
  - job_name: 'election-intelligence'
    metrics_path: '/api/v1/metrics'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:8000']
```
