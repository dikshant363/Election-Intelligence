# Streaming Gateway, WebSockets & SSE Guide

## Overview

The Streaming Gateway manages real-time client connections using WebSockets and Server-Sent Events (SSE), offering topic-based channel subscriptions and presence tracking.

---

## Supported Streaming Mechanisms

### 1. WebSockets (`/api/v1/ws`)
- **Protocol**: Bi-directional JSON streaming.
- **Client Actions**:
  - `{"action": "subscribe", "topic": "results"}`
  - `{"action": "unsubscribe", "topic": "results"}`
  - `{"action": "ping"}` -> Server responds `{"type": "pong"}`
- **Heartbeat & Reconnect**: Periodic ping broadcasts detect disconnected or idle sockets.

### 2. Server-Sent Events (`/api/v1/stream?topic=results`)
- **Protocol**: Unidirectional HTTP stream (`text/event-stream`).
- **Format**:
  ```text
  event: ResultPublished
  data: {"event_id": "...", "payload": {...}}
  ```

---

## Live Channel Topics

- `elections`: Live election status changes and schedule updates
- `results`: Live vote count and result publication updates
- `candidates`: Candidate updates and affidavit changes
- `analytics`: Turnout aggregations and state/party statistics
- `ai_notifications`: Real-time AI RAG processing notifications
- `system_notifications`: Platform alerts and system maintenance messages

---

## Backpressure & Slow Consumer Mitigation

The `BackpressureController` protects the system by:
- Enforcing rate limits per client (default: max `50` msg/sec).
- Capping outbound socket queue depth (default: max `100` queued items).
- Dropping messages and logging slow consumer metrics when overflow occurs.
