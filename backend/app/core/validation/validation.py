"""Core validation contracts and containers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ValidationError:
    """Individual validation failure detail."""

    field: str
    message: str
    code: str = "INVALID_FIELD"


@dataclass(frozen=True)
class ValidationResult:
    """Container holding validation outcome and error list."""

    is_valid: bool
    errors: list[ValidationError] = field(default_factory=list)

    @classmethod
    def valid(cls) -> "ValidationResult":
        """Factory for a successful ValidationResult."""
        return cls(is_valid=True, errors=[])

    @classmethod
    def invalid(cls, errors: list[ValidationError]) -> "ValidationResult":
        """Factory for a failed ValidationResult."""
        return cls(is_valid=False, errors=errors)


class Validator[T](ABC):
    """Abstract generic validator contract."""

    @abstractmethod
    async def validate(self, instance: T) -> ValidationResult:
        """Validate an entity instance asynchronously."""
        pass
