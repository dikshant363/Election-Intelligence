# Deployment Runbook: Election Intelligence Platform

## 1. Pre-Deployment Checklist
- [ ] CI pipeline (`pytest` 287 tests) passed.
- [ ] Database migrations (`alembic`) tested against a staging database clone.
- [ ] Secrets and environment variables (`DATABASE_URL`, `REDIS_URL`, `ENVIRONMENT`, `ENABLE_HSTS`) verified in target environment.
- [ ] Rollback plan documented and approved.
- [ ] Notification sent to `#engineering-deployments`.

## 2. Development Deployment
Use this for local development and integration testing.
```bash
# Rebuild images and start detached
docker compose up --build -d

# Run migrations locally
docker compose exec backend alembic upgrade head
```

## 3. Staging Deployment
Staging requires strict adherence to environment parity.
```bash
export ENVIRONMENT=staging
export IMAGE_TAG=v1.0.0-rc.1

# Pull target image
docker compose pull backend

# Run migrations (ensure completion before traffic shift)
docker compose run --rm backend alembic upgrade head

# Deploy
docker compose up -d backend
```

## 4. Production Deployment
1. Silence non-critical alerts in PagerDuty.
2. Verify primary database health: `curl -s https://api.civiclens.in/api/v1/health`.
3. Export production tags:
```bash
export ENVIRONMENT=production
export IMAGE_TAG=v1.0.0
export ENABLE_HSTS=true
export SECURE_COOKIES=true
export LOG_LEVEL=INFO
```
4. Run migrations from a dedicated ephemeral container:
```bash
docker compose run --rm backend alembic upgrade head
```
5. Perform rolling update:
```bash
docker compose up -d --no-deps --build backend
```
6. Verify deployment via `/api/v1/diagnostics`.

## 5. Blue-Green Deployment Procedure
*Requires a reverse proxy / load balancer (e.g., Nginx, Traefik).*
1. Deploy `v-next` backend stack (Green) alongside `v-current` (Blue).
2. Wait for Green `/api/v1/ready` to return 200 OK.
3. Update load balancer config to point 100% traffic to Green.
4. Reload load balancer (`nginx -s reload`).
5. Terminate Blue stack after 15 minutes of stable Green metrics.

## 6. Canary Deployment Procedure
1. Deploy `v-next` to a single node.
2. Route 5% of traffic to the Canary node.
3. Monitor metrics at `/api/v1/metrics` (Prometheus) for 15 minutes:
   - Check HTTP 5xx rate on Canary vs Primary.
   - Check P99 latency on Canary vs Primary.
4. If metrics degrade > 10%, instantly drain Canary traffic (Rollback trigger).
5. If stable, increase traffic routing (25% -> 50% -> 100%).

## 7. Database Migration Procedure
Database changes are strictly forward-only.
1. **Backup:** `pg_dump -U postgres -d election_intel -F c -f pre_deploy.dump`
2. **Execute:** `alembic upgrade head`
3. **Verify:** Run a quick read query on the altered table.
4. **Rollback (if needed):** `alembic downgrade -1` (only if data destruction is explicitly avoided in the script).

## 8. Rollback Procedure
If the deployment fails or metrics degrade severely:
```bash
# 1. Identify previous stable tag
export IMAGE_TAG=v0.9.5

# 2. Re-deploy previous image
docker compose up -d --no-deps backend

# 3. Revert database schema ONLY IF REQUIRED AND SAFE
docker compose run --rm backend alembic downgrade <previous_revision_id>

# 4. Flush cache to prevent schema mismatch serialization errors
docker compose exec redis redis-cli FLUSHDB
```

## 9. Disaster Recovery Procedure
**Targets:** RTO: 1 hour | RPO: 15 minutes.
1. Stop all backend containers to prevent split-brain data writes.
2. Restore database from the latest automated volume snapshot or WAL archive:
```bash
pg_restore -U postgres -d election_intel -1 -c backup_snapshot.dump
```
3. Boot the backend services and check `/api/v1/diagnostics`.
4. Run data integrity checks on user credentials and audit logs.

## 10. Post-Deployment Verification
For 30 minutes following the deployment, SRE must monitor:
- [ ] **Grafana Dashboards:** API latency, error rates, DB connection pool utilization.
- [ ] **OpenTelemetry APM:** Check for anomalous spans or n+1 query regressions.
- [ ] **Smoke Tests:** Execute a login flow, a data search, and an admin dashboard load.
