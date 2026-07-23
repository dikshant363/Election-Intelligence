# Incident Response Playbook

## 1. Incident Severity Levels

| Severity | Definition | SLA (Acknowledge) | SLA (Mitigate) |
| :--- | :--- | :--- | :--- |
| **SEV-0 (P0)** | Core platform down. Total outage, zero availability. | 5 minutes | 30 minutes |
| **SEV-1 (P1)** | Critical feature broken (Auth, Search) affecting many users. | 15 minutes | 1 hour |
| **SEV-2 (P2)** | Performance degradation, minor feature failure. | 1 hour | 4 hours |
| **SEV-3 (P3)** | Non-user facing issue, internal tool failure, cosmetic bugs. | 24 hours | 7 days |

## 2. Incident Response Process
1. **Detect:** Alerts trigger via Prometheus/OpenTelemetry, or user reports.
2. **Triage:** Acknowledge alert, assign Incident Commander (IC), determine Severity.
3. **Mitigate:** Apply immediate fixes (rollback, scale up, block IPs) to restore service. *Do not try to root-cause during mitigation.*
4. **Resolve:** Implement the actual bug fix or structural repair.
5. **Postmortem:** Conduct blameless RCA within 48 hours.

## 3. Communication Templates

**Internal Alert (Slack `#incidents`)**
> 🚨 **[SEV-X] <Short Description>**
> **Impact:** <What is broken>
> **Incident Commander:** @<Name>
> **Zoom Bridge:** <Link>

**Status Page Update (External)**
> **Investigating:** We are currently investigating reports of <issue>. Our engineering team is actively working to resolve this. Next update in 15 minutes.

**Stakeholder Update (Email/Exec Slack)**
> **Update:** The issue affecting <system> has been mitigated via <action>. Service is fully restored. A full postmortem will be provided by <Date>.

## 4. Specific Incident Playbooks

### Service Completely Down (API returning 5xx)
1. Check Cloudflare/WAF layer for blocks.
2. Check `docker compose ps` to see if backend containers are OOM or CrashLoopBackOff.
3. Check DB capacity; if maxed out, restart backend to kill orphaned connections.
4. *Mitigation:* Rollback to previous known-good deployment immediately.

### Database Connection Failure
1. Verify PostgreSQL container is running and port 5432 is bound.
2. Check `DATABASE_URL` environment variables.
3. Review logs for `psycopg2.OperationalError` or `asyncpg.exceptions.TooManyConnectionsError`.
4. *Mitigation:* Restart app nodes, increase `max_connections` in `postgresql.conf` if historically justified.

### Authentication Service Failure
1. Check IdP (Identity Provider) status pages.
2. Inspect `backend/app/observability/alerts` for JWT validation errors.
3. Verify JWT Secret hasn't been accidentally rotated or truncated.
4. *Mitigation:* Issue emergency comms, rollback recent auth-related PRs.

### Data Breach Detected
1. **IMMEDIATE:** Lock down all external access (enable maintenance mode WAF rule).
2. Revoke all active sessions (Flush Redis session cache).
3. Rotate DB credentials, API keys, and JWT `SECRET_KEY`.
4. Preserve logs (OpenTelemetry, DB Audit logs) for forensics.
5. Notify Legal and DPO within 1 hour.

### Performance Degradation (Latency Spike)
1. Identify the slow endpoint via OpenTelemetry spans.
2. Check Redis hit rate; if 0%, Redis might be down.
3. Run `EXPLAIN ANALYZE` on suspected slow database queries.
4. *Mitigation:* Apply rate limiting aggressively via CacheService, add missing DB index concurrently.

### Search Returning Wrong Results
1. Check background synchronization worker status.
2. *Mitigation:* Rebuild the search index using the capacity planner utility script: `python -m app.performance.capacity_planner rebuild_index`.

### AI Guardrails Bypassed
1. Immediately disable AI feature flags via Redis configuration keys.
2. Review logs to capture the prompt injection payload.
3. *Mitigation:* Update prompt filters/circuit breakers in `backend/app/production/` before re-enabling.

## 5. Postmortem Template
- **Incident ID / Name:**
- **Date & Duration:**
- **Impact:** (e.g., "5,000 users unable to login for 22 minutes")
- **Root Cause:** (e.g., "Missing index on users table caused table scan, exhausting connections")
- **Timeline:** (List exact UTC timestamps of detection, mitigation, resolution)
- **Action Items:** (List JIRA tickets, owners, and due dates to prevent recurrence)

## 6. Rollback Decision Matrix

| Condition | Action | Justification |
| :--- | :--- | :--- |
| Bug is strictly localized, fix is known and tested | **Fix-Forward** | Faster than full revert cycle |
| Root cause unknown, affecting core flows | **Rollback** | Prioritize SLA and user experience |
| Database schema already mutated and destructive | **Fix-Forward** | Rollback would cause data loss |
| Deployment < 5 mins ago, severe errors present | **Rollback** | Safest default stance |

## 7. Contact Escalation Path
1. **L1 Support / On-Call SRE:** Acknowledges within 5m.
2. **L2 Application Engineer:** Escalated to if bug is in application logic (15m).
3. **L3 Staff Engineer / DB Admin:** Escalated to for complex distributed systems failures or data corruption (30m).
4. **L4 VP Engineering:** Escalated to for SEV-0 incidents lasting > 1 hour.
