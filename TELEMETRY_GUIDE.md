# TelemetryContext & Distributed Tracing Guide

## Overview

The `TelemetryContext` and `TracerProvider` abstractions provide distributed tracing capabilities compatible with OpenTelemetry collectors, Jaeger, Tempo, and Zipkin.

---

## TelemetryContext Specification

Every request, event, and background job carries a `TelemetryContext`:

```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "span_id": "4a71644665544000",
  "correlation_id": "c1234567-89ab-cdef-0123-456789abcdef",
  "causation_id": "cmd_8812",
  "request_id": "req_9918",
  "user_id": "usr_election_admin",
  "session_id": "sess_1001",
  "service": "election-intelligence",
  "component": "api",
  "environment": "production"
}
```

---

## HTTP Header Propagation

The `ObservabilityMiddleware` extracts incoming trace headers and automatically injects them into outgoing HTTP responses:

- `X-Trace-ID`
- `X-Span-ID`
- `X-Correlation-ID`

---

## Programmatic Span Instrumenting

```python
from app.observability.tracing import global_tracer

with global_tracer.start_span("process_election_data", component="etl") as span:
    span.attributes["record_count"] = 500
```
