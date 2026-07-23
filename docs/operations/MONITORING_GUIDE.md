# Monitoring & Observability Guide

This document outlines the monitoring, observability, and alerting strategies for the Election Intelligence Platform v1.0.0.

## 1. Observability Philosophy

Our observability strategy is built on the three pillars:
- **Metrics:** Quantitative data (counters, gauges, histograms) used for alerting and dashboards (via Prometheus).
- **Logs:** Discrete, structured JSON events providing context about system behavior and errors.
- **Traces:** End-to-end request flows across distributed components (via OpenTelemetry).

## 2. Health Probes

The FastAPI backend exposes several endpoints to monitor application state. These conform to standard Kubernetes probe definitions:

- `/api/v1/health`: Basic health check. Returns `200 OK` if the web server is running. Used to verify the process is alive.
- `/api/v1/ready`: Readiness check. Verifies connections to the database and Redis. Returns `200 OK` if ready to accept traffic, or `503 Service Unavailable` otherwise. Used by Load Balancers.
- `/api/v1/live`: Liveness check. Ensures the app hasn't deadlocked. Used to trigger container restarts.
- `/api/v1/diagnostics`: Deep diagnostic endpoint providing version info, environment details, and dependency latency. Not for automated polling.

## 3. Prometheus Metrics

Metrics are exposed at `/api/v1/metrics`. Key metrics include:

| Metric Name | Type | Description | Alert Threshold |
|---|---|---|---|
| `http_requests_total` | Counter | Total number of HTTP requests. | N/A |
| `http_request_duration_seconds` | Histogram | Latency of HTTP requests. | P99 > 500ms |
| `db_connection_pool_usage` | Gauge | Active vs available DB connections. | > 80% capacity |
| `cache_hit_ratio` | Gauge | Redis cache hit percentage. | < 70% |
| `ai_query_duration_seconds` | Histogram | Latency of external LLM calls. | P95 > 5s |
| `error_rate_total` | Counter | Total HTTP 5xx responses. | > 1% of total reqs |

## 4. OpenTelemetry Tracing

We use OpenTelemetry for distributed tracing. 
- **Trace Capture:** Every HTTP request generates a root span. Database queries, Redis calls, and external AI queries generate child spans.
- **Context Propagation:** We use W3C Trace Context (`traceparent` header).
- **Viewing Traces:** Traces are exported to an OTEL Collector and can be viewed in Jaeger or Datadog. Search by `trace_id` included in HTTP response headers.

## 5. Structured JSON Logging

Logs are emitted in structured JSON format via `backend/app/logging.py`.
- **Format:** `{"timestamp": "...", "level": "INFO", "logger": "app.api", "message": "...", "trace_id": "..."}`
- **Log Levels:** `DEBUG` (development), `INFO` (production state changes), `WARNING` (client errors, retries), `ERROR` (unhandled exceptions, system failures).
- **Search:** JSON structure allows querying in Elasticsearch/Kibana or Datadog (e.g., `level:ERROR AND path:"/api/v1/ai/query"`).

## 6. Alert Definitions

Alerts should be routed to PagerDuty/Slack based on severity:
- **High Severity (Page):**
  - Availability < 99.9% over 5m.
  - HTTP 5xx Error Rate > 1% over 5m.
  - Database connection pool > 90% for 2m.
- **Low Severity (Ticket):**
  - Cache hit ratio < 50% for 15m.
  - P99 Latency > 500ms for 10m.
  - CPU/Memory usage > 80%.

## 7. Dashboard Recommendations

The main Ops Dashboard (Grafana) should display:
- **Top Row (Golden Signals):** Request Rate (RPS), Error Rate (%), P99 Latency, Active Users.
- **Middle Row (Infrastructure):** CPU Usage, Memory Usage, DB Pool Usage, Redis Memory.
- **Bottom Row (Application):** AI Query Latency, Cache Hit Ratio, ETL Job Status, Search Index Size.

## 8. Health Check Automation

- **Kubernetes / ECS:** 
  - Set `livenessProbe` to `/api/v1/live` (initialDelay: 10s, period: 10s).
  - Set `readinessProbe` to `/api/v1/ready` (initialDelay: 5s, period: 5s).
- **Load Balancer (AWS ALB / Nginx):** Route traffic only to targets passing the `/api/v1/ready` check.

## 9. Log Aggregation

Logs are written to `stdout`/`stderr` by default. 
- In Docker Compose, configure the logging driver to forward to Fluentd or AWS CloudWatch.
- Do not write logs to local files in production to avoid disk exhaustion.

## 10. SLO/SLI Definitions

Service Level Objectives (SLOs) and Indicators (SLIs):
- **Availability:** 99.9% uptime (SLI: successful requests / total requests).
- **Latency:** 99% of requests < 500ms (SLI: `http_request_duration_seconds` P99).
- **Data Freshness:** ETL pipeline completes within 1 hour (SLI: time since last successful run).
