"""Background task contracts and placeholder implementations."""

import asyncio
from abc import ABC, abstractmethod
from typing import Any


class Task[T](ABC):
    """Abstract background task interface."""

    def __init__(self, task_id: str, name: str) -> None:
        self.task_id = task_id
        self.name = name

    @abstractmethod
    async def execute(self) -> T:
        """Execute task logic asynchronously."""
        pass


class TaskScheduler(ABC):
    """Abstract task scheduler interface."""

    @abstractmethod
    async def schedule(
        self,
        task: Task[Any],
        delay_seconds: float = 0.0,
    ) -> str:
        """Schedule a task for execution."""
        pass


class Worker(ABC):
    """Abstract background task worker interface."""

    @abstractmethod
    async def start(self) -> None:
        """Start worker execution loop."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop worker execution loop."""
        pass

    @abstractmethod
    async def process_next(self) -> bool:
        """Process the next available queued task."""
        pass


class InMemoryTaskScheduler(TaskScheduler):
    """Placeholder in-memory task scheduler implementation."""

    def __init__(self) -> None:
        self._queue: list[Task[Any]] = []

    async def schedule(
        self,
        task: Task[Any],
        delay_seconds: float = 0.0,
    ) -> str:
        """Schedule task in memory queue."""
        if delay_seconds > 0:
            await asyncio.sleep(0.0)  # Async non-blocking yield placeholder
        self._queue.append(task)
        return task.task_id


class InMemoryWorker(Worker):
    """Placeholder in-memory task worker implementation."""

    def __init__(self, scheduler: InMemoryTaskScheduler) -> None:
        self._scheduler = scheduler
        self._is_running = False

    async def start(self) -> None:
        """Mark worker as running."""
        self._is_running = True

    async def stop(self) -> None:
        """Mark worker as stopped."""
        self._is_running = False

    async def process_next(self) -> bool:
        """Process next task in memory queue."""
        if self._scheduler._queue:
            task = self._scheduler._queue.pop(0)
            await task.execute()
            return True
        return False
