# Disaster Recovery & Resilience Guide

## Overview

The `BackupManager`, `ResiliencePolicy`, and `CircuitBreaker` subsystems guarantee platform resilience and recovery against system failures.

---

## Backup Snapshot Lifecycle

```python
from app.production.backup import global_backup_manager

# Create snapshot with SHA-256 integrity checksum
meta = global_backup_manager.create_snapshot(payload=b"db_dump")

# Verify checksum integrity
is_valid = global_backup_manager.verify_snapshot(meta.backup_id, payload=b"db_dump")
```

---

## Circuit Breaker State Machine

```text
       [Normal Operations]
                │
         Success│ (Failure Threshold Exceeded)
                ▼
            ┌──────┐
            │ CLOSED │
            └──────┘
               │
               │ (Threshold Exceeded)
               ▼
            ┌──────┐
            │ OPEN │ ─── (Recovery Time Elapsed) ──► ┌───────────┐
            └──────┘                                 │ HALF-OPEN │
                                                     └───────────┘
                                                           │ (Success)
                                                           ▼
                                                       [CLOSED]
```

When circuit breaker is `OPEN`, operations fail fast with `CircuitBreakerOpenError` without overloading downstream databases or services.
