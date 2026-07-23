# ADMINISTRATIVE API REFERENCE
## Enterprise Control Center — Version 1.0.0

---

## Overview

The Control Center APIs are exposed under the `/api/v1/admin` path prefix. All endpoints enforce strict RBAC authorization and structured JSON request/response formats.

---

## Endpoint Specification

### 1. Control Center Overview Telemetry
- **Method**: `GET`
- **Path**: `/api/v1/admin/overview`
- **Summary**: Returns consolidated platform system telemetry, active entity counts, worker status, and Redis cache hit ratios.
- **Response**: `200 OK`
```json
{
  "platform_name": "Election Intelligence Platform",
  "version": "1.0.0",
  "environment": "production",
  "status": "OPERATIONAL",
  "system_health": {
    "cpu_utilization_percent": 14.2,
    "memory_utilization_percent": 38.5,
    "disk_free_gb": 57.0,
    "database_pool_active": 5,
    "redis_latency_ms": 1.2
  },
  "entity_counts": {
    "elections": 24,
    "constituencies": 543,
    "candidates": 8420,
    "parties": 120
  },
  "active_workers": 4
}
```

---

### 2. Feature Flags Management
- **Method**: `GET`
- **Path**: `/api/v1/admin/feature-flags`
- **Summary**: Lists all active platform feature toggles.

- **Method**: `POST`
- **Path**: `/api/v1/admin/feature-flags/{flag_name}/toggle`
- **Body**: `{"enabled": boolean}`
- **Summary**: Dynamically enables or disables a platform feature toggle without downtime.

---

### 3. Security Audit Logs
- **Method**: `GET`
- **Path**: `/api/v1/admin/security/audit-logs?limit=20`
- **Summary**: Retrieves recent security audit entries including actor, action, resource, status, and IP address.

---

### 4. AI Control Center Status
- **Method**: `GET`
- **Path**: `/api/v1/admin/ai/status`
- **Summary**: Returns active LLM provider routing (`openai`, `gemini`, `claude`, `ollama`), token consumption, cache hit rate, and guardrail status.

---

### 5. System Operations
- **Method**: `POST`
- **Path**: `/api/v1/admin/ops/flush-cache`
- **Summary**: Flushes Redis and memory query caches.

- **Method**: `POST`
- **Path**: `/api/v1/admin/ops/reindex`
- **Summary**: Triggers full-text search (SAL) and vector store reindexing.

---

### 6. Executive Strategic KPIs
- **Method**: `GET`
- **Path**: `/api/v1/admin/executive/kpis`
- **Summary**: Provides high-level strategic intelligence KPIs, national turnout metrics, and regional insights for executive dashboards.
