# Election Intelligence Platform (v1.0.0)

[![CI/CD Pipeline](https://github.com/CivicLens-India/Election-Intelligence/actions/workflows/ci.yml/badge.svg)](https.github.com/CivicLens-India/Election-Intelligence/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/CivicLens-India/Election-Intelligence)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An enterprise-grade, production-ready Election Intelligence Platform designed for multi-tier election data ingestion, full-text search, spatial queries, hybrid AI retrieval (RAG), real-time event streaming, observability, distributed caching, security controls, and cross-platform mobile apps.

---

## Key Features

- **Clean Architecture & Domain Driven Design**: Strict separation of Domain, Application, Infrastructure, and Transport layers.
- **Data Ingestion & ETL**: High-performance validation, cleaning, and batch import pipelines for election results and candidate records.
- **Search & Discovery Platform**: Full-text search with BM25 scoring, recency decay, autocomplete, and geospatial bounding box / polygon queries.
- **AI Intelligence Platform**: Hybrid BM25 + Vector RAG engine with source attributions, safety guardrails, and evaluation.
- **Real-Time Event Streaming**: Standardized `EventEnvelope` architecture supporting WebSockets, Server-Sent Events (`SSE`), and client presence tracking.
- **Observability & Operations**: OpenTelemetry tracing, Prometheus metrics, structured JSON logging, and health probes (`/health`, `/ready`, `/live`, `/diagnostics`).
- **Performance & Scalability**: Vendor-independent `CacheService` (Memory & Redis), event-driven tag invalidation, sliding window rate limiting, capacity planning, and load benchmarking.
- **Production Hardening**: `SecretsProvider` abstraction, startup configuration fingerprinting, SHA-256 backup snapshot integrity, SPDX 2.3 SBOM, and circuit breaker resilience.
- **Cross-Platform Mobile App**: Flutter Material 3, Riverpod state management, GoRouter navigation, and offline caching.

---

## Quick Start

### 1. Docker Compose Execution (Recommended)
```bash
docker compose up -d --build
```
API Documentation available at: `http://localhost:8000/docs`

### 2. Local Backend Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=backend uvicorn app.main:app --reload --port 8000
```

### 3. Flutter Application Setup
```bash
cd frontend
flutter pub get
flutter run
```

---

## Verification & Testing

```bash
# Run backend linters & tests
ruff check backend
python -m compileall backend
pytest

# Run frontend linters & tests
cd frontend
flutter analyze
flutter test
```

---

## Documentation

- **[PRODUCTION_RELEASE_GUIDE.md](file:///Users/dikshantagarwal/Desktop/CivicLens%20India/Election-Intelligence/PRODUCTION_RELEASE_GUIDE.md)**: Production Deployment & Architecture Guide
- **[SYSTEM_INTEGRATION_MATRIX.md](file:///Users/dikshantagarwal/Desktop/CivicLens%20India/Election-Intelligence/SYSTEM_INTEGRATION_MATRIX.md)**: Subsystem Integration Mapping
- **[CHANGELOG.md](file:///Users/dikshantagarwal/Desktop/CivicLens%20India/Election-Intelligence/CHANGELOG.md)**: Full Version Release History
- **[openapi.json](file:///Users/dikshantagarwal/Desktop/CivicLens%20India/Election-Intelligence/openapi.json)**: OpenAPI v3.1 Specification