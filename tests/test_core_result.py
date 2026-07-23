"""Unit tests for shared core Result monad and DomainError types."""

import pytest
from app.core.result import DomainError, ErrorCode, Failure, Result, Success


def test_result_ok_creation() -> None:
    """Verify Result.ok instantiation and immutability."""
    res = Result.ok("data_payload")
    assert res.is_success is True
    assert res.is_failure is False
    assert res.value == "data_payload"
    assert res.unwrap() == "data_payload"
    assert res.unwrap_or("fallback") == "data_payload"


def test_result_fail_creation() -> None:
    """Verify Result.fail instantiation and error propagation."""
    err = DomainError(code=ErrorCode.NOT_FOUND, message="Resource not found")
    res: Result[str] = Result.fail(err)
    assert res.is_success is False
    assert res.is_failure is True
    assert res.error == err
    assert res.unwrap_or("fallback") == "fallback"


def test_result_value_access_on_failure_raises() -> None:
    """Verify accessing .value on a failed Result raises ValueError."""
    err = DomainError(code=ErrorCode.BAD_REQUEST, message="Bad request")
    res: Result[int] = Result.fail(err)

    with pytest.raises(ValueError, match="Cannot access value of a failed Result"):
        _ = res.value


def test_result_error_access_on_success_raises() -> None:
    """Verify accessing .error on a successful Result raises ValueError."""
    res = Result.ok(42)

    with pytest.raises(ValueError, match="Cannot access error of a successful Result"):
        _ = res.error


def test_success_and_failure_dataclasses() -> None:
    """Verify Success and Failure containers."""
    succ = Success(value=100)
    assert succ.is_success is True
    assert succ.value == 100

    err = DomainError(code=ErrorCode.INTERNAL_ERROR, message="Error")
    fail = Failure(error=err)
    assert fail.is_failure is True
    assert fail.error.code == ErrorCode.INTERNAL_ERROR
