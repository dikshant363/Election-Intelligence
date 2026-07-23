"""Unit tests for background task interfaces and memory worker."""

import pytest
from app.core.tasks import InMemoryTaskScheduler, InMemoryWorker, Task


class DummyTask(Task[str]):
    def __init__(self, task_id: str, name: str, result_box: list[str]) -> None:
        super().__init__(task_id, name)
        self.result_box = result_box

    async def execute(self) -> str:
        self.result_box.append(f"executed_{self.task_id}")
        return f"executed_{self.task_id}"


@pytest.mark.asyncio
async def test_in_memory_task_scheduler_and_worker() -> None:
    """Verify task scheduling and worker processing."""
    scheduler = InMemoryTaskScheduler()
    worker = InMemoryWorker(scheduler)
    results: list[str] = []

    task = DummyTask("t1", "test_task", results)
    task_id = await scheduler.schedule(task)
    assert task_id == "t1"

    await worker.start()
    processed = await worker.process_next()
    assert processed is True
    assert results == ["executed_t1"]

    # Process empty queue
    assert await worker.process_next() is False
    await worker.stop()
