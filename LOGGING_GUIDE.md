# Structured JSON Logging & Secret Redaction Guide

## Overview

The logging framework outputs single-line JSON log events enriched with `TelemetryContext` metadata and automatic secret sanitization.

---

## JSON Log Schema Example

```json
{
  "timestamp": "2026-07-23T12:00:00.000Z",
  "severity": "INFO",
  "message": "Processed candidate query",
  "service": "election-intelligence",
  "component": "api",
  "environment": "production",
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "span_id": "4a71644665544000",
  "correlation_id": "c1234567-89ab-cdef-0123-456789abcdef",
  "causation_id": "",
  "request_id": "req_9918",
  "user_id": null
}
```

---

## Secret Sanitization

The `sanitize_dict` function automatically redacts sensitive key patterns (`password`, `secret`, `token`, `api_key`, `authorization`, `bearer`):

```json
{
  "username": "admin",
  "password": "[REDACTED_SECRET]",
  "api_key": "[REDACTED_SECRET]"
}
```
