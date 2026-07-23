"""Shared domain result types and error codes."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, TypeVar

T = TypeVar("T")


class ErrorCode(StrEnum):
    """Standard domain error codes."""

    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    CONFLICT = "CONFLICT"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    TIMEOUT = "TIMEOUT"
    BAD_REQUEST = "BAD_REQUEST"


@dataclass(frozen=True)
class DomainError:
    """Immutable domain error representation."""

    code: ErrorCode
    message: str
    details: dict[str, Any] | None = None


@dataclass(frozen=True)
class Success[T]:
    """Successful operation result container."""

    value: T
    is_success: bool = True
    is_failure: bool = False


@dataclass(frozen=True)
class Failure:
    """Failed operation result container."""

    error: DomainError
    is_success: bool = False
    is_failure: bool = True


class Result[T]:
    """Generic immutable Result monad container for application operations."""

    def __init__(
        self,
        value: T | None = None,
        error: DomainError | None = None,
        is_success: bool = True,
    ) -> None:
        if is_success and error is not None:
            raise ValueError("Successful result cannot contain an error.")
        if not is_success and error is None:
            raise ValueError("Failed result must contain a DomainError.")

        self._value = value
        self._error = error
        self._is_success = is_success

    @property
    def is_success(self) -> bool:
        """Return True if the result represents a success."""
        return self._is_success

    @property
    def is_failure(self) -> bool:
        """Return True if the result represents a failure."""
        return not self._is_success

    @property
    def value(self) -> T:
        """Return the value if successful, raises ValueError if failed."""
        if not self._is_success or self._value is None:
            raise ValueError("Cannot access value of a failed Result.")
        return self._value

    @property
    def error(self) -> DomainError:
        """Return the DomainError if failed, raises ValueError if successful."""
        if self._is_success or self._error is None:
            raise ValueError("Cannot access error of a successful Result.")
        return self._error

    @classmethod
    def ok(cls, value: T) -> "Result[T]":
        """Factory method for creating a successful Result."""
        return cls(value=value, error=None, is_success=True)

    @classmethod
    def fail(cls, error: DomainError) -> "Result[T]":
        """Factory method for creating a failed Result."""
        return cls(value=None, error=error, is_success=False)

    def unwrap(self) -> T:
        """Unwrap the value if successful, or raise RuntimeError with the error message."""
        if self.is_failure:
            raise RuntimeError(f"Result failed: {self.error.message}")
        return self.value

    def unwrap_or(self, default: T) -> T:
        """Return the value if successful, or the default value if failed."""
        if self.is_failure:
            return default
        return self.value

    def __repr__(self) -> str:
        if self._is_success:
            return f"Result.ok({self._value!r})"
        return f"Result.fail({self._error!r})"
