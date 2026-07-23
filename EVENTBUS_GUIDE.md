# EventBus & EventEnvelope Standard Guide

## Overview

The `EventBus` provides a vendor-independent messaging abstraction for publishing, subscribing, and replaying domain events across the platform.

---

## EventEnvelope Standard

Every message published across WebSockets, SSE, background queues, or future message brokers (Redis Streams, Kafka, NATS) adheres to the `EventEnvelope` specification:

```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "ResultPublished",
  "event_version": "v1.0",
  "aggregate_id": "res_9918",
  "timestamp": "2026-07-23T12:00:00Z",
  "correlation_id": "c1234567-89ab-cdef-0123-456789abcdef",
  "causation_id": "cmd_8812",
  "producer": "election-intelligence-platform",
  "payload": {
    "election_id": "el_2024_ls",
    "candidate_id": "cand_varanasi_1",
    "votes": 612970
  },
  "metadata": {
    "priority": "high",
    "state_code": "UP"
  }
}
```

---

## Domain Event Types

| Event Type | Aggregate ID | Purpose |
| :--- | :--- | :--- |
| `ElectionCreated` | `election_id` | Fired when a new election is configured |
| `ElectionUpdated` | `election_id` | Fired on election status/schedule change |
| `ResultPublished` | `result_id` | Fired when vote counts or results are published |
| `CandidateUpdated` | `candidate_id` | Fired on candidate details update |
| `PartyUpdated` | `party_id` | Fired on political party info update |
| `PollingBoothUpdated` | `booth_id` | Fired on polling booth configuration change |
| `ImportCompleted` | `job_id` | Fired when ETL data ingestion finishes |
| `SearchIndexUpdated` | `index_name` | Fired when search index is updated |
| `AIEvaluationCompleted` | `eval_id` | Fired when AI RAG evaluation metrics complete |

---

## Replay Capability

The `InMemoryEventBus` maintains an in-memory event store per topic allowing clients to replay past events from a specified timestamp or fetch recent history for reconnection recovery.
