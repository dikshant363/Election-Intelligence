# Infrastructure Guide

This guide details the infrastructure architecture of the Election Intelligence Platform.

## 1. Infrastructure Overview

The platform leverages a containerized microservices architecture:
- **Backend API**: FastAPI (Python 3.12) running under Uvicorn.
- **Primary Database**: PostgreSQL 15, managed via SQLAlchemy 2 and AsyncPG.
- **Cache / Message Broker**: Redis 7.
- **Observability**: OpenTelemetry for tracing, Prometheus for metrics.
- *(Optional)* **Search**: OpenSearch for advanced text search.
- *(Optional)* **Storage**: S3-compatible object storage for database backups and static assets.

## 2. Local Development Infrastructure

Local development is orchestrated via `docker-compose.yml` at the project root.

- **`api` service**: Runs the FastAPI application. Exposes port `8000`. Mounts `./backend/app` as a volume for hot-reloading. Includes a health check endpoint `/health`.
- **`db` service**: PostgreSQL 15. Exposes port `5432`. Uses a named volume `pgdata` for persistence.
- **`redis` service**: Redis 7. Exposes port `6379`. Uses a named volume `redisdata`.
- **`prometheus` service**: Scrapes metrics from the API on port `9090`.

## 3. Container Architecture

- **API Container**: Based on `python:3.12-slim`. Runs Uvicorn. The `PYTHONPATH` is set to `/app/backend` to ensure the 15 subsystems are correctly resolved. Runs as a non-root user.
- **DB Container**: Based on `postgres:15-alpine`. Configured for performance (shared buffers, work_mem). Persistent volume mounted at `/var/lib/postgresql/data`.
- **Cache Container**: Based on `redis:7-alpine`. Configured with AOF (Append Only File) persistence for durability.

## 4. Network Topology

In Docker Compose, all services share a custom bridge network (`election_net`).
- The `api` container can communicate with `db` and `redis`.
- The `db` and `redis` containers do not expose ports to the host machine in production, only to the internal network.
- The `prometheus` container can reach the `api` container to scrape metrics.

## 5. Volume Strategy

- **PostgreSQL Data**: Persistent volume to ensure election data survives container restarts. Requires strict backup policies.
- **Redis Data**: Persistent volume for AOF to preserve session data and rate-limiting counters.

## 6. Environment Variable Injection

- **Development**: Uses a `.env` file loaded by `docker-compose`.
- **Production**: Secrets (DB passwords, API keys) are injected via CI/CD pipelines (GitHub Actions) or a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault) into container environment variables. Never commit `.env` files.

## 7. Resource Requirements

| Component | Minimum (Dev) | Recommended (Production) |
|---|---|---|
| **API Instance** | 1 CPU, 1GB RAM | 4+ CPU, 8GB RAM (per instance) |
| **Database** | 1 CPU, 2GB RAM | 4+ CPU, 16GB RAM, Fast NVMe SSD |
| **Redis** | 0.5 CPU, 512MB RAM | 2 CPU, 4GB RAM |
| **Full Stack** | 2 CPU, 4GB RAM | Horizontally scaled as needed |

## 8. Scaling Architecture

The FastAPI application is stateless. To scale:
1. Deploy multiple API container replicas.
2. Place an Application Load Balancer (ALB) or NGINX reverse proxy in front of the instances.
3. Configure sticky sessions if required by the frontend, though token-based auth (JWT) allows stateless load balancing.
4. Scale PostgreSQL via read replicas for heavy read workloads (common during election results).

## 9. Health Check Configuration

- **Docker Compose**: Uses the `HEALTHCHECK` directive hitting `/health` on the API container.
- **Kubernetes**: 
  - *Liveness Probe*: HTTP GET `/health/liveness` (returns 200 if the app is running).
  - *Readiness Probe*: HTTP GET `/health/readiness` (returns 200 if DB and Redis are connected).

## 10. Kubernetes Migration Path

Moving from `docker-compose` to Kubernetes (K8s) requires:
1. **Deployments**: Define replicas for the `api` service.
2. **Services**: Create ClusterIP services for internal routing and a LoadBalancer/Ingress for external API access.
3. **ConfigMaps**: Store non-sensitive configuration variables.
4. **Secrets**: Store DB credentials and API keys.
5. **StatefulSets/PVCs**: Use StatefulSets and PersistentVolumeClaims for PostgreSQL and Redis, though managed services (e.g., AWS RDS, ElastiCache) are strongly recommended for production databases.

## 11. Observability Infrastructure

- **Metrics**: Prometheus scrapes the `/metrics` endpoint exposed by the FastAPI app (using `prometheus-client`).
- **Tracing**: OpenTelemetry auto-instruments FastAPI, SQLAlchemy, and AsyncPG, sending traces to an OTLP collector (e.g., Jaeger or Datadog).
- **Logs**: JSON formatted logs output to `stdout`/`stderr`, aggregated by tools like Promtail/Loki or Fluentd/Elasticsearch.

## 12. Backup Infrastructure

- **Database**: Scheduled cron jobs run `pg_dump` daily.
- **Storage**: Backups are compressed and pushed to object storage (e.g., AWS S3).
- **Retention**: Keep daily backups for 30 days, weekly for 6 months, and yearly backups indefinitely for historical election records.
