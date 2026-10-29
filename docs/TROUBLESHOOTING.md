# Election Intelligence Platform — Troubleshooting & Runbook
**Version:** 1.0.0 (Phase 26 Canonical Baseline)  
**Scope:** Local Development, Docker Containers, PostgreSQL 17, and Free Cloud Deployment

---

## 1. Quick Diagnostic Checklist

Run this command sequence to instantly determine system status:

```bash
# 1. Check live application process
curl -s -i http://localhost:3000/ready

# 2. Check PostgreSQL connection
pg_isready -h localhost -p 5432 -d election_intelligence

# 3. Check database migrations status
psql -d election_intelligence -c "SELECT COUNT(*) FROM elections;"

# 4. Check system test suite
cargo test --all-features
```

---

## 2. Common Issues, Root Causes & Verified Fixes

### Issue 1: "relation 'elections' does not exist" on Clean Database
- **Symptom:** Application starts but queries to `/candidates`, `/constituencies`, or `/api/v1/elections` fail with database error 500.
- **Root Cause:** Prior to Phase 26, database migrations were only applied through external manual `psql` scripts. A clean database or fresh cloud deployment had no tables created.
- **Verified Fix:** In Phase 26, `Database::run_migrations(&self)` was embedded directly into the Rust binary. Upon startup, the binary automatically executes migrations `0001`, `0002`, and `0003` idempotently using `CREATE TABLE IF NOT EXISTS` and `ON CONFLICT DO NOTHING`.
- **Manual Verification:**
  ```bash
  psql -d election_intelligence -f migrations/0001_initial_schema.sql
  psql -d election_intelligence -f migrations/0002_seed_initial_data.sql
  psql -d election_intelligence -f migrations/0003_authentic_2024_lok_sabha_data.sql
  ```

---

### Issue 2: Cloud Health Check Probe Fails (HTTP 404 or HTML Returned)
- **Symptom:** Cloud providers (Render, Fly, AWS, Kubernetes) report container unhealthy because health probe returns HTML or non-200.
- **Root Cause:** Probing `/health` or `/ready` was captured by the HTML root fallback handler rather than dedicated health check endpoints.
- **Verified Fix:** In Phase 26, dedicated lightweight JSON endpoints were added:
  - `/ready` and `/api/v1/ready`: Returns HTTP 200 `{"status": "READY", "database": "CONNECTED"}` if PostgreSQL responds to `SELECT 1`; returns HTTP 503 if disconnected.
  - `/health` and `/api/v1/health`: Returns detailed system telemetry and component health.
- **Test Command:**
  ```bash
  curl -i http://localhost:3000/ready
  ```

---

### Issue 3: Ingestion Endpoint Returns 401 UNAUTHORIZED
- **Symptom:** Calling `POST /api/v1/etl/ingest` or `PATCH /api/v1/corrections/:id/review` returns HTTP 401 with message: `"Administrative authorization required"`.
- **Root Cause:** Administrative write endpoints are protected by token authorization.
- **Verified Fix:** Include the `Authorization: Bearer <ADMIN_API_KEY>` header or `X-Admin-Key: <ADMIN_API_KEY>`.
- **Example:**
  ```bash
  curl -X POST http://localhost:3000/api/v1/etl/ingest \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer admin_secret_token_2026" \
    -d @batch.json
  ```

---

### Issue 4: Port Binding Conflicts or Missing Cloud `PORT`
- **Symptom:** Application fails to start on cloud providers with error `Address already in use` or cloud provider fails to route incoming requests.
- **Root Cause:** Hardcoding port 3000 when cloud providers like Render inject `PORT=10000` or Cloud Run injects `PORT=8080`.
- **Verified Fix:** `src/config.rs` reads `PORT` from the environment dynamically:
  ```rust
  let port = env::var("PORT").ok().and_then(|p| p.parse().ok()).unwrap_or(3000);
  ```
  And binds to `0.0.0.0` by default.

---

### Issue 5: PostgreSQL TLS Handshake Error with Neon / Supabase
- **Symptom:** `error: connection reset by peer` or `SSL connection required`.
- **Root Cause:** Cloud providers (Neon, Supabase) require TLS encrypted connections.
- **Verified Fix:** Append `?sslmode=require` to `DATABASE_URL`. The application binary is compiled with `tls-rustls` enabled in `Cargo.toml`, ensuring cross-platform native TLS without external dynamic OpenSSL library dependencies.
  ```
  DATABASE_URL=postgres://user:password@ep-pooler.region.neon.tech/election_intelligence?sslmode=require
  ```

---

## 3. Disaster Recovery & Database Backup / Restore

```bash
# To create an immutable, timestamped database backup with SHA-256 checksum:
./scripts/backup_postgres.sh ./backups

# To verify archive checksum and restore database:
./scripts/restore_postgres.sh ./backups/election_intelligence_backup_YYYYMMDD_HHMMSSZ.sql.gz
```
