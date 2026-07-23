"""Base async repository interfaces."""

from abc import ABC, abstractmethod
from collections.abc import Sequence


class ReadRepository[T, ID](ABC):
    """Abstract async read-only repository contract."""

    @abstractmethod
    async def get_by_id(self, entity_id: ID) -> T | None:
        """Retrieve an entity by its unique identifier."""
        pass

    @abstractmethod
    async def find_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[T]:
        """Retrieve a paginated collection of entities."""
        pass

    @abstractmethod
    async def count(self) -> int:
        """Count total entities in storage."""
        pass

    @abstractmethod
    async def exists(self, entity_id: ID) -> bool:
        """Check if an entity with the given identifier exists."""
        pass


class WriteRepository[T, ID](ABC):
    """Abstract async write-only repository contract."""

    @abstractmethod
    async def add(self, entity: T) -> T:
        """Persist a new entity to storage."""
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Update an existing persisted entity in storage."""
        pass

    @abstractmethod
    async def delete(self, entity: T) -> None:
        """Delete an entity instance from storage."""
        pass

    @abstractmethod
    async def delete_by_id(self, entity_id: ID) -> bool:
        """Delete an entity by its unique identifier."""
        pass


class Repository[T, ID](ReadRepository[T, ID], WriteRepository[T, ID], ABC):
    """Abstract combined async CRUD repository contract."""

    pass
