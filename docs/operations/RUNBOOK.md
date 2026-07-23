# Operational Runbook: Election Intelligence Platform v1.0.0

## 1. Service Overview
The Election Intelligence Platform is an asynchronous FastAPI application serving AI-driven insights, real-time search, and administrative dashboards.

**Service Level Agreements (SLAs):**
*   **API P99 Latency:** < 100ms
*   **Search P99 Latency:** < 200ms
*   **Dashboard Load (Full Dataset):** < 1s
*   **Availability:** 99.99%

## 2. Health Check Procedures
Health endpoints are mounted under `/api/v1/`. Use these to determine application state.

```bash
# Basic liveness probe (K8s/Docker liveness)
curl -s http://localhost:8000/api/v1/live | jq

# Readiness probe (verifies DB & Redis connections)
curl -s http://localhost:8000/api/v1/ready | jq

# Deep diagnostics (connection pools, memory usage, cache hit rate)
curl -s http://localhost:8000/api/v1/diagnostics | jq
```

## 3. Common Operational Tasks

### Restart Backend Service
```bash
docker compose restart backend
```

### Check and Tail Logs
Logs are emitted in JSON format via `backend/app/logging.py`.
```bash
docker compose logs -f --tail=100 backend | jq .
```

### Connect to PostgreSQL
```bash
docker compose exec db psql -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-election_intel}
```
*Diagnostic Query (Active Queries):*
```sql
SELECT pid, age(clock_timestamp(), query_start), usename, query 
FROM pg_stat_activity 
WHERE state != 'idle' AND query NOT ILIKE '%pg_stat_activity%' 
ORDER BY query_start desc;
```

### Flush Redis Cache
Used to mitigate persistent cache poisoning or stale global states.
```bash
docker compose exec redis redis-cli FLUSHDB
```

### Rotate JWT Secrets
1. Update `SECRET_KEY` in the vault/environment.
2. Restart backend nodes on a rolling basis. Note: This will invalidate all active user sessions unless dual-key verification is temporarily enabled in `SecretsProvider`.

### Trigger Manual Backup
```bash
docker compose exec backend python -m app.production.backup_snapshot
```

## 4. Alert Response Playbooks

| Alert Name | Detection | Mitigation |
| :--- | :--- | :--- |
| **Database Connection Exhausted** | `pg_stat_pool` > 90% in Prometheus | 1. Check `/diagnostics` for leaked sessions.<br>2. Kill idle queries in Postgres.<br>3. Temporarily increase `pool_size` in `DATABASE_URL`. |
| **High Memory Usage** | Backend RAM > 85% | 1. Capture memory profile via APM.<br>2. Restart backend container if OOM imminent.<br>3. Check CacheService keys for unbounded growth. |
| **Slow API Response** | P99 > 100ms for 5m | 1. Check `OpenTelemetry` traces for DB lock waits.<br>2. Check `redis` latency.<br>3. Trigger autoscaling engine if CPU bound. |
| **Auth Failures Spike** | 401/403 rate > 5% | 1. Verify `SECURE_COOKIES` and `ENVIRONMENT` match.<br>2. Check IdP upstream status.<br>3. Review Rate Limiter blocks. |
| **Search Index Behind** | Index lag > 1000 records | 1. Check background task worker queues.<br>2. Manually trigger index sync script. |
| **Cache Miss Rate High** | Miss rate > 40% | 1. Verify Redis connectivity and eviction policies.<br>2. Verify memory limit on Redis instance. |

## 5. Escalation Matrix

| Domain | Primary Contact | Secondary Contact | Channels |
| :--- | :--- | :--- | :--- |
| **Database / PostgreSQL** | DBA On-Call | Platform Engineering | `#db-ops`, PagerDuty |
| **Security / Auth** | SecOps Lead | Staff Engineer | `#security-alerts`, PagerDuty |
| **Infra / Docker / Redis**| SRE On-Call | Platform Engineering | `#infra-alerts`, PagerDuty |
| **Data / Search Issues** | Data Engineering | Backend On-Call | `#data-ops`, Slack |

## 6. Useful Diagnostic Commands

```bash
# View active container status
docker compose ps

# Check Redis memory stats
docker compose exec redis redis-cli info memory

# Evaluate backend resource usage
docker stats --no-stream

# Force circuit breaker reset (via Python console)
docker compose exec backend python -c "from app.production.circuit_breakers import reset_all; reset_all()"
```
