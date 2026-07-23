# Service Level Objectives and Indicators (SLO & SLI)

## 1. SLO Philosophy

The Election Intelligence Platform prioritizes reliability and performance. Our SLOs define the acceptable level of reliability for our users. We use **Error Budgets** to balance feature velocity with platform stability. If an error budget is exhausted, feature deployments are halted in favor of reliability engineering tasks until the budget recovers.

## 2. SLI Definitions

### Availability SLI
- **Definition:** The percentage of successful requests to critical endpoints.
- **Measurement:** Percentage of `/api/v1/health` and core API requests returning HTTP 2xx or 3xx in 5-minute windows.

### API Latency SLI
- **Definition:** The response time for standard API requests.
- **Measurement:** P50, P95, and P99 response times of all `/api/v1/*` endpoints, measured at the API Gateway.

### Search Latency SLI
- **Definition:** The response time for complex election search queries.
- **Measurement:** P95 response time of `/api/v1/search` endpoint.

### Auth Latency SLI
- **Definition:** The time required to process authentication requests.
- **Measurement:** P95 response time of login and token refresh requests.

### Error Rate SLI
- **Definition:** The proportion of requests resulting in server errors.
- **Measurement:** Percentage of HTTP 5xx responses over total requests (excluding 4xx client errors).

## 3. SLO Targets Table

| Service | SLI | SLO Target | Error Budget (30 days) |
|---------|-----|------------|------------------------|
| **API Gateway** | Availability | 99.9% | ~43 minutes of downtime |
| **Core API** | API Latency (P99) | < 100ms | 1% of requests > 100ms |
| **Search Engine**| Search Latency (P95) | < 200ms | 5% of requests > 200ms |
| **Identity/Auth**| Auth Latency (P95) | < 100ms | 5% of requests > 100ms |
| **All Services** | Error Rate | < 0.1% | 0.1% of total requests |
| **Mobile App** | Startup Time | < 2.0s | 5% of cold starts > 2.0s |
| **Web Dashboard**| TTI (Time to Interactive) | < 1.0s | 5% of loads > 1.0s |

## 4. Error Budget Policy

- **< 50% Consumed:** Normal operations. Feature velocity prioritized.
- **50% - 90% Consumed:** Warning state. Team reviews recent deployments for instability.
- **> 90% Consumed:** Alert state. Principal Architect notified. High-risk deployments paused.
- **> 100% Consumed (Exhausted):** Code freeze. Only bug fixes and reliability improvements can be deployed until the 30-day rolling window recovers the budget.

## 5. SLO Measurement Windows

All SLOs are measured over a **rolling 30-day window**. This ensures that short-term spikes are balanced against long-term stability, preventing permanent penalty for isolated incidents.

## 6. Alert Thresholds

- **Page (Critical):** Error budget burn rate is 10x normal, indicating budget will exhaust in 3 days. Availability drops below 99.0% for 15 minutes.
- **Ticket (High):** Error budget burn rate is 2x normal. P99 latency exceeds SLO for 1 hour.
- **Log (Informational):** Transient spikes in error rate or latency that auto-resolve within 5 minutes.

## 7. SLO Review Process

- **Cadence:** Monthly SLO Review Meeting.
- **Attendees:** Platform Engineering Lead, Product Manager, DevOps Engineer.
- **Agenda:** Review previous month's performance, analyze budget burns, adjust targets if necessary, prioritize reliability work.

## 8. Prometheus Queries (PromQL)

**Availability SLI:**
```promql
sum(rate(http_requests_total{status=~"2..|3.."}[5m])) / sum(rate(http_requests_total[5m]))
```

**API Latency (P99):**
```promql
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{path=~"/api/v1/.*"}[5m])) by (le))
```

**Error Rate SLI:**
```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total{status!~"4.."}[5m]))
```

## 9. Dashboard Specification

The Grafana SLO Dashboard must include:
- Global Service Health Indicator (Red/Yellow/Green).
- Remaining Error Budget (Gauge chart).
- Availability over 30 days (Line chart).
- Latency heatmaps for Core API, Search, and Auth.
- Top 5 highest latency endpoints table.
- Error rate trend line vs threshold line.

## 10. SLO Violation Postmortem Requirements

Any incident that consumes more than 20% of the 30-day error budget requires a blameless postmortem. The postmortem must detail:
- Root cause analysis (Five Whys).
- Impact duration and severity.
- Remediation steps taken.
- Action items to prevent recurrence (assigned to specific engineers with deadlines).
