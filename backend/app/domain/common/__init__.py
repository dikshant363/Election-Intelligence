"""Common domain abstractions package initialization."""

from app.domain.common.base import (
    AggregateRoot,
    Entity,
    Identifier,
    Timestamp,
    ValueObject,
)

__all__ = [
    "AggregateRoot",
    "Entity",
    "Identifier",
    "Timestamp",
    "ValueObject",
]
