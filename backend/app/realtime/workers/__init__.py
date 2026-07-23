"""Background Worker, Job Queue, Exponential Backoff, and Dead-Letter Queue."""

from __future__ import annotations

import asyncio
import contextlib
import logging
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger("app.realtime.workers")


@dataclass
class Job:
    """Background task job container."""

    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "default_job"
    payload: dict[str, Any] = field(default_factory=dict)
    attempts: int = 0
    max_retries: int = 3
    backoff_factor: float = 1.5
    created_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
    status: str = "pending"  # pending, running, completed, failed, cancelled
    error: str | None = None


@dataclass
class DeadLetterJob:
    """Dead-letter queue job container."""

    job: Job
    failed_at: str
    final_error: str


class DeadLetterQueue:
    """Stores failed jobs after max retries are exhausted."""

    def __init__(self) -> None:
        self._dead_letters: list[DeadLetterJob] = []

    def add(self, job: Job, error: str) -> None:
        dl = DeadLetterJob(
            job=job,
            failed_at=datetime.now(UTC).isoformat(),
            final_error=error,
        )
        self._dead_letters.append(dl)
        logger.warning("Job %s moved to DeadLetterQueue: %s", job.job_id, error)

    def list_jobs(self) -> list[DeadLetterJob]:
        return list(self._dead_letters)


class BackgroundWorker:
    """Background worker executing async jobs with retries and exponential backoff."""

    def __init__(self, dlq: DeadLetterQueue | None = None) -> None:
        self.dlq = dlq or DeadLetterQueue()
        self._queue: asyncio.Queue[tuple[Job, Callable[[Job], Awaitable[None]]]] = asyncio.Queue()
        self._running = False
        self._worker_task: asyncio.Task[None] | None = None
        self._cancelled_jobs: set[str] = set()

    async def enqueue(self, job: Job, handler: Callable[[Job], Awaitable[None]]) -> None:
        """Enqueue job for background execution."""
        await self._queue.put((job, handler))

    def cancel_job(self, job_id: str) -> None:
        """Cancel a pending/running job by ID."""
        self._cancelled_jobs.add(job_id)

    async def start(self) -> None:
        """Start worker background processing loop."""
        self._running = True
        self._worker_task = asyncio.create_task(self._process_loop())

    async def stop(self) -> None:
        """Gracefully stop worker."""
        self._running = False
        if self._worker_task:
            self._worker_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._worker_task

    async def _process_loop(self) -> None:
        while self._running:
            try:
                job, handler = await asyncio.wait_for(self._queue.get(), timeout=0.5)
            except TimeoutError:
                continue

            if job.job_id in self._cancelled_jobs:
                job.status = "cancelled"
                self._queue.task_done()
                continue

            await self._execute_with_retry(job, handler)
            self._queue.task_done()

    async def _execute_with_retry(
        self, job: Job, handler: Callable[[Job], Awaitable[None]]
    ) -> None:
        job.status = "running"
        while job.attempts <= job.max_retries:
            job.attempts += 1
            try:
                await handler(job)
                job.status = "completed"
                return
            except Exception as err:  # noqa: BLE001
                job.error = str(err)
                if job.attempts > job.max_retries:
                    job.status = "failed"
                    self.dlq.add(job, str(err))
                    return

                # Calculate exponential backoff sleep
                delay = (job.backoff_factor ** (job.attempts - 1)) if job.backoff_factor >= 1.0 else 0.001
                logger.info(
                    "Retrying job %s attempt %d/%d after %.2fs",
                    job.job_id,
                    job.attempts,
                    job.max_retries,
                    delay,
                )
                await asyncio.sleep(delay)

        job.status = "failed"
        self.dlq.add(job, job.error or "Max retries reached")
