"""Unit tests for base async repository interface abstractions."""

from collections.abc import Sequence
from dataclasses import dataclass

import pytest
from app.core.repositories import Repository


@dataclass
class DummyEntity:
    id: int
    name: str


class InMemoryDummyRepository(Repository[DummyEntity, int]):
    """Concrete in-memory implementation of abstract Repository contract for testing."""

    def __init__(self) -> None:
        self._items: dict[int, DummyEntity] = {}

    async def get_by_id(self, entity_id: int) -> DummyEntity | None:
        return self._items.get(entity_id)

    async def find_all(self, skip: int = 0, limit: int = 100) -> Sequence[DummyEntity]:
        values = list(self._items.values())
        return values[skip : skip + limit]

    async def count(self) -> int:
        return len(self._items)

    async def exists(self, entity_id: int) -> bool:
        return entity_id in self._items

    async def add(self, entity: DummyEntity) -> DummyEntity:
        self._items[entity.id] = entity
        return entity

    async def update(self, entity: DummyEntity) -> DummyEntity:
        self._items[entity.id] = entity
        return entity

    async def delete(self, entity: DummyEntity) -> None:
        self._items.pop(entity.id, None)

    async def delete_by_id(self, entity_id: int) -> bool:
        return self._items.pop(entity_id, None) is not None


@pytest.mark.asyncio
async def test_repository_contract_crud_operations() -> None:
    """Verify repository contract method execution."""
    repo = InMemoryDummyRepository()
    entity = DummyEntity(id=1, name="Test")

    # Add & Count
    await repo.add(entity)
    assert await repo.count() == 1
    assert await repo.exists(1) is True

    # Get & Find All
    retrieved = await repo.get_by_id(1)
    assert retrieved is not None
    assert retrieved.name == "Test"

    all_items = await repo.find_all()
    assert len(all_items) == 1

    # Update
    updated_entity = DummyEntity(id=1, name="Updated Test")
    await repo.update(updated_entity)
    assert (await repo.get_by_id(1)).name == "Updated Test"

    # Delete
    deleted = await repo.delete_by_id(1)
    assert deleted is True
    assert await repo.count() == 0
