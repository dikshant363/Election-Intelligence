# Real-Time Intelligence & Event Streaming Platform Guide

## Overview

The **Real-Time Intelligence Platform** (`backend/app/realtime/`) enables event-driven communication, live election updates, WebSocket & SSE streaming, background processing with exponential backoff, presence tracking, and backpressure rate-limiting across the Election Intelligence Platform.

---

## Architectural Principles

```text
Database / System Actions
         ↓
  Domain Events (EventEnvelope Standard)
         ↓
      EventBus (InMemoryEventBus / Redis / Kafka)
         ↓
  ┌──────┴─────────────────────────┐
  ▼                                ▼
Background Workers        Streaming Gateway (WebSockets / SSE)
  │                                │
  ▼                                ▼
Job Queue & DLQ               Live Connected Clients
```

1. **Dedicated Module Isolation**: All realtime mechanisms reside strictly inside `backend/app/realtime/`.
2. **EventEnvelope Standard**: Every event uses a vendor-agnostic envelope with `event_id`, `event_type`, `aggregate_id`, `timestamp`, `correlation_id`, `causation_id`, `producer`, `payload`, and `metadata`.
3. **Layer Independence**: Existing domain, application, search, and AI layers publish events without depending on transport implementations.

---

## Core Real-Time Components

| Component | Location | Purpose |
| :--- | :--- | :--- |
| **EventBus** | `backend/app/realtime/eventbus/` | Pub/sub bus with topic isolation and replay event log |
| **Domain Events** | `backend/app/realtime/events/` | Immutable domain event constructors wrapped in `EventEnvelope` |
| **Workers & DLQ** | `backend/app/realtime/workers/` | Async `BackgroundWorker` with retries, exponential backoff, and `DeadLetterQueue` |
| **Streaming** | `backend/app/realtime/streaming/` | WebSocket `ConnectionManager` and SSE stream generator |
| **Presence** | `backend/app/realtime/presence/` | Client connection tracking, topic subscriptions, and heartbeat ping/pong |
| **Backpressure** | `backend/app/realtime/backpressure/` | Outbound queue bounds, rate limiting per client, and slow consumer detection |
| **Notifications** | `backend/app/realtime/notifications/` | Prioritized alert delivery service |
| **Metrics** | `backend/app/realtime/metrics/` | Connected client count, throughput, dropped messages, queue depth |

---

## API & WebSocket Endpoints

- `GET /api/v1/events` — Replay historical events for a topic
- `GET /api/v1/stream` — Subscribe to Server-Sent Events (SSE) stream
- `WS /api/v1/ws` — Real-time WebSocket topic channel endpoint
- `POST /api/v1/events/publish` — Publish custom event to EventBus & clients
- `GET /api/v1/realtime/presence` — View active connected client presence
- `GET /api/v1/realtime/metrics` — View system throughput and queue metrics
