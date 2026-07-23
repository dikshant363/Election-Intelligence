# Observability, Telemetry & Operations Platform Guide

## Overview

The **Observability Platform** (`backend/app/observability/`) provides end-to-end operational visibility across all REST APIs, Search queries, AI RAG operations, Realtime event streaming, ETL pipelines, and background workers.

---

## Architectural Principles

```text
Application Operations (REST, AI, Search, ETL, Realtime, Workers)
         ↓
  TelemetryContext (trace_id, span_id, correlation_id, causation_id)
         ↓
  ┌──────┴─────────────────────────┐
  ▼                                ▼
TracerProvider / Spans      Prometheus Metrics & Alerts
  │                                │
  ▼                                ▼
Structured JSON Logs         Exposition Endpoint /api/v1/metrics
```

1. **Dedicated Module Isolation**: All telemetry mechanisms reside strictly inside `backend/app/observability/`.
2. **Unified Telemetry Context**: Propagates `trace_id`, `span_id`, `correlation_id`, `causation_id`, `request_id`, `user_id`, `service`, and `component` across all execution flows.
3. **Non-Invasive Instrumentation**: Instruments the platform via `ObservabilityMiddleware` and `TelemetryService` without mutating domain business logic.

---

## Core Components

| Component | Location | Purpose |
| :--- | :--- | :--- |
| **TelemetryContext** | `backend/app/observability/telemetry/` | Standardized trace context specification and async propagation |
| **Tracing** | `backend/app/observability/tracing/` | OpenTelemetry `TracerProvider` and `Span` lifecycle management |
| **Metrics** | `backend/app/observability/metrics/` | Prometheus metrics collection and text exposition generator |
| **Logging** | `backend/app/observability/logging/` | Structured JSON logger with secret redaction |
| **Health** | `backend/app/observability/health/` | Liveness (`/live`) and readiness (`/ready`) diagnostic probes |
| **Diagnostics** | `backend/app/observability/diagnostics/` | Runtime status, uptime, dependency graph, and feature flags |
| **Alerting** | `backend/app/observability/alerts/` | Threshold-based alert rules (`AlertManager`) |
| **Middleware** | `backend/app/observability/middleware/` | FastAPI automatic request tracing & span context propagation |

---

## API Endpoints

- `GET /api/v1/health` — Full platform readiness check with component dependency status
- `GET /api/v1/ready` — Readiness probe for load balancers
- `GET /api/v1/live` — Instant liveness probe
- `GET /api/v1/metrics` — Prometheus text-based exposition metrics endpoint
- `GET /api/v1/diagnostics` — Runtime configuration and feature flag status
- `GET /api/v1/alerts` — Configured alert rules and firing status
