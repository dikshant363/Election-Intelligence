# Background Workers, Retries & Dead-Letter Queue Guide

## Overview

The `BackgroundWorker` system executes asynchronous background tasks (such as ETL processing, index updates, report generation, and notification dispatch) with retry logic, exponential backoff, and dead-letter queue (DLQ) support.

---

## Worker Architecture

```text
Enqueue Job (Job Queue)
         │
         ▼
Worker Execution Loop
         │
         ├──► Success ──► Job Status = "completed"
         │
         └──► Failure ──► Attempts <= MaxRetries?
                                │
                                ├── Yes ──► Exponential Backoff Sleep ──► Retry
                                │
                                └── No  ──► Move to DeadLetterQueue (DLQ)
```

---

## Exponential Backoff Calculation

For attempt $n$:

$$\text{Delay} = \text{backoff\_factor}^{(n - 1)}$$

Default configuration:
- `max_retries`: `3`
- `backoff_factor`: `1.5` (Delays: 1.0s, 1.5s, 2.25s)

---

## Dead-Letter Queue (DLQ)

Jobs that fail after exhausting all retry attempts are safely isolated in the `DeadLetterQueue` along with error stack traces, execution timestamp, and job payload for inspection and manual replay.
