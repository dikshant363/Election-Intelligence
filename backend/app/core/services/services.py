"""Core service interfaces."""

import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class ClockService(ABC):
    """Abstract clock service interface for time operations."""

    @abstractmethod
    def now(self) -> datetime:
        """Return current local datetime."""
        pass

    @abstractmethod
    def utcnow(self) -> datetime:
        """Return current UTC datetime with timezone info."""
        pass


class UUIDService(ABC):
    """Abstract UUID generation service interface."""

    @abstractmethod
    def generate_v4(self) -> uuid.UUID:
        """Generate a random UUID version 4."""
        pass

    @abstractmethod
    def generate_v7(self) -> uuid.UUID:
        """Generate a time-ordered UUID version 7."""
        pass


class HashService(ABC):
    """Abstract hashing service interface for security utilities."""

    @abstractmethod
    def hash_string(self, value: str) -> str:
        """Generate a cryptographic hash of string value."""
        pass

    @abstractmethod
    def verify_hash(self, value: str, hashed: str) -> bool:
        """Verify string value against a cryptographic hash."""
        pass


class Serializer[T](ABC):
    """Abstract serialization service interface."""

    @abstractmethod
    def serialize(self, obj: T) -> str:
        """Serialize an object instance to a string format."""
        pass

    @abstractmethod
    def deserialize(self, data: str) -> T:
        """Deserialize a string representation into an object instance."""
        pass


class ConfigurationService(ABC):
    """Abstract configuration service interface."""

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a configuration parameter value by key."""
        pass
