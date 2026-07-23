"""Unit tests for validation layer objects."""

import pytest

from app.core.validation import ValidationError, ValidationResult, Validator


class DummyValidator(Validator[str]):
    async def validate(self, instance: str) -> ValidationResult:
        if not instance:
            return ValidationResult.invalid(
                [ValidationError(field="text", message="Text cannot be empty")]
            )
        return ValidationResult.valid()


@pytest.mark.asyncio
async def test_validation_result_valid_and_invalid() -> None:
    """Verify ValidationResult factories and Validator execution."""
    validator = DummyValidator()

    valid_res = await validator.validate("hello")
    assert valid_res.is_valid is True
    assert len(valid_res.errors) == 0

    invalid_res = await validator.validate("")
    assert invalid_res.is_valid is False
    assert len(invalid_res.errors) == 1
    assert invalid_res.errors[0].field == "text"
    assert invalid_res.errors[0].message == "Text cannot be empty"
