"""ETL tracking: import progress and job state management."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class JobStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


@dataclass
class JobProgress:
    """Mutable in-memory progress tracker for a running ETL job."""

    job_id: uuid.UUID
    job_name: str
    status: JobStatus = JobStatus.PENDING
    total_records: int = 0
    parsed_records: int = 0
    valid_records: int = 0
    rejected_records: int = 0
    loaded_records: int = 0
    current_chunk: int = 0
    total_chunks: int = 0
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    log_entries: list[str] = field(default_factory=list)

    def start(self) -> None:
        self.status = JobStatus.RUNNING
        self.started_at = datetime.now(UTC)

    def complete(self) -> None:
        self.status = JobStatus.COMPLETED
        self.completed_at = datetime.now(UTC)

    def fail(self, message: str) -> None:
        self.status = JobStatus.FAILED
        self.error_message = message
        self.completed_at = datetime.now(UTC)

    def cancel(self) -> None:
        self.status = JobStatus.CANCELLED
        self.completed_at = datetime.now(UTC)

    def log(self, message: str) -> None:
        ts = datetime.now(UTC).strftime("%H:%M:%S")
        self.log_entries.append(f"[{ts}] {message}")

    @property
    def progress_pct(self) -> float:
        if self.total_records == 0:
            return 0.0
        return round(self.loaded_records / self.total_records * 100, 1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": str(self.job_id),
            "job_name": self.job_name,
            "status": self.status.value,
            "total_records": self.total_records,
            "parsed_records": self.parsed_records,
            "valid_records": self.valid_records,
            "rejected_records": self.rejected_records,
            "loaded_records": self.loaded_records,
            "progress_pct": self.progress_pct,
            "current_chunk": self.current_chunk,
            "total_chunks": self.total_chunks,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error_message": self.error_message,
        }


class JobRegistry:
    """In-memory registry of active and recent ETL jobs."""

    def __init__(self) -> None:
        self._jobs: dict[uuid.UUID, JobProgress] = {}

    def register(self, job_name: str) -> JobProgress:
        job_id = uuid.uuid4()
        progress = JobProgress(job_id=job_id, job_name=job_name)
        self._jobs[job_id] = progress
        return progress

    def get(self, job_id: uuid.UUID) -> JobProgress | None:
        return self._jobs.get(job_id)

    def all_jobs(self) -> list[dict[str, Any]]:
        return [job.to_dict() for job in self._jobs.values()]

    def cancel(self, job_id: uuid.UUID) -> bool:
        job = self._jobs.get(job_id)
        if job and job.status == JobStatus.RUNNING:
            job.cancel()
            return True
        return False


# Singleton registry for the application lifetime
job_registry = JobRegistry()
