"""ETL validation engine: schema, type, range, duplicate, geographic, cross-reference checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# Geographic coordinate bounds
_LAT_MIN = -90.0
_LAT_MAX = 90.0
_LON_MIN = -180.0
_LON_MAX = 180.0


@dataclass
class FieldRule:
    """Defines validation rules for a single field."""

    name: str
    required: bool = True
    field_type: type | None = None
    min_value: float | None = None
    max_value: float | None = None
    allowed_values: set[str] | None = None
    max_length: int | None = None


@dataclass
class ValidationReport:
    """Human-readable validation result for an import batch."""

    total_records: int = 0
    valid_records: int = 0
    invalid_records: int = 0
    errors: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.invalid_records == 0

    @property
    def error_rate(self) -> float:
        if self.total_records == 0:
            return 0.0
        return self.invalid_records / self.total_records


def _check_required(
    rule: FieldRule, value: Any, record_index: int
) -> dict[str, Any] | None:
    if rule.required and (value is None or str(value).strip() == ""):
        return {
            "record": record_index,
            "field": rule.name,
            "error": "REQUIRED_FIELD_MISSING",
            "message": f"Required field '{rule.name}' is missing or empty.",
        }
    return None


def _check_type(
    rule: FieldRule, value: Any, record_index: int
) -> dict[str, Any] | None:
    if rule.field_type is None:
        return None
    try:
        rule.field_type(value)
    except (ValueError, TypeError):
        return {
            "record": record_index,
            "field": rule.name,
            "error": "TYPE_MISMATCH",
            "message": (
                f"Field '{rule.name}' value '{value}' "
                f"cannot be cast to {rule.field_type.__name__}."
            ),
        }
    return None


def _check_range(
    rule: FieldRule, value: Any, record_index: int
) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if rule.min_value is None and rule.max_value is None:
        return errors
    try:
        num = float(value)
        if rule.min_value is not None and num < rule.min_value:
            errors.append(
                {
                    "record": record_index,
                    "field": rule.name,
                    "error": "RANGE_BELOW_MIN",
                    "message": (
                        f"Field '{rule.name}' value {num} "
                        f"is below minimum {rule.min_value}."
                    ),
                }
            )
        if rule.max_value is not None and num > rule.max_value:
            errors.append(
                {
                    "record": record_index,
                    "field": rule.name,
                    "error": "RANGE_ABOVE_MAX",
                    "message": (
                        f"Field '{rule.name}' value {num} "
                        f"exceeds maximum {rule.max_value}."
                    ),
                }
            )
    except (ValueError, TypeError):
        pass
    return errors


def _check_allowed(
    rule: FieldRule, value: Any, record_index: int
) -> dict[str, Any] | None:
    if rule.allowed_values is None:
        return None
    str_val = str(value).strip()
    if str_val not in rule.allowed_values:
        return {
            "record": record_index,
            "field": rule.name,
            "error": "INVALID_VALUE",
            "message": (
                f"Field '{rule.name}' value '{str_val}' "
                f"not in allowed set: {sorted(rule.allowed_values)[:5]}..."
            ),
        }
    return None


def _check_length(
    rule: FieldRule, value: Any, record_index: int
) -> dict[str, Any] | None:
    if rule.max_length is None:
        return None
    str_val = str(value)
    if len(str_val) > rule.max_length:
        return {
            "record": record_index,
            "field": rule.name,
            "error": "VALUE_TOO_LONG",
            "message": (
                f"Field '{rule.name}' value length {len(str_val)} "
                f"exceeds max {rule.max_length}."
            ),
        }
    return None


class RecordValidator:
    """Validates individual records against a set of FieldRules."""

    def __init__(self, rules: list[FieldRule]) -> None:
        self.rules = rules

    def validate_record(
        self, record: dict[str, Any], record_index: int
    ) -> list[dict[str, Any]]:
        """Return list of error dicts for a single record."""
        errors: list[dict[str, Any]] = []

        for rule in self.rules:
            value = record.get(rule.name)

            req_error = _check_required(rule, value, record_index)
            if req_error:
                errors.append(req_error)
                continue

            if value is None or str(value).strip() == "":
                continue

            type_error = _check_type(rule, value, record_index)
            if type_error:
                errors.append(type_error)
                continue

            errors.extend(_check_range(rule, value, record_index))

            allowed_error = _check_allowed(rule, value, record_index)
            if allowed_error:
                errors.append(allowed_error)

            length_error = _check_length(rule, value, record_index)
            if length_error:
                errors.append(length_error)

        return errors


class DuplicateDetector:
    """Detects duplicate records based on composite key fields."""

    def __init__(self, key_fields: list[str]) -> None:
        self.key_fields = key_fields
        self._seen: set[tuple[str, ...]] = set()

    def is_duplicate(self, record: dict[str, Any]) -> bool:
        key = tuple(str(record.get(f, "")).strip() for f in self.key_fields)
        if key in self._seen:
            return True
        self._seen.add(key)
        return False

    def reset(self) -> None:
        self._seen.clear()


class GeographicValidator:
    """Validates geographic coordinate fields."""

    @staticmethod
    def validate_lat_lon(
        record: dict[str, Any],
        lat_field: str,
        lon_field: str,
        record_index: int,
    ) -> list[dict[str, Any]]:
        errors: list[dict[str, Any]] = []
        lat_val = record.get(lat_field)
        lon_val = record.get(lon_field)

        if lat_val is not None and str(lat_val).strip():
            try:
                lat = float(lat_val)
                if not (_LAT_MIN <= lat <= _LAT_MAX):
                    errors.append(
                        {
                            "record": record_index,
                            "field": lat_field,
                            "error": "INVALID_LATITUDE",
                            "message": f"Latitude {lat} out of valid range [-90, 90].",
                        }
                    )
            except (ValueError, TypeError):
                errors.append(
                    {
                        "record": record_index,
                        "field": lat_field,
                        "error": "INVALID_LATITUDE_FORMAT",
                        "message": f"Latitude '{lat_val}' is not a valid number.",
                    }
                )

        if lon_val is not None and str(lon_val).strip():
            try:
                lon = float(lon_val)
                if not (_LON_MIN <= lon <= _LON_MAX):
                    errors.append(
                        {
                            "record": record_index,
                            "field": lon_field,
                            "error": "INVALID_LONGITUDE",
                            "message": f"Longitude {lon} out of valid range [-180, 180].",
                        }
                    )
            except (ValueError, TypeError):
                errors.append(
                    {
                        "record": record_index,
                        "field": lon_field,
                        "error": "INVALID_LONGITUDE_FORMAT",
                        "message": f"Longitude '{lon_val}' is not a valid number.",
                    }
                )

        return errors


class BatchValidator:
    """Orchestrates record-level validation + duplicate detection for an entire batch."""

    def __init__(
        self,
        rules: list[FieldRule],
        duplicate_key_fields: list[str] | None = None,
        geo_config: tuple[str, str] | None = None,
    ) -> None:
        self.validator = RecordValidator(rules)
        self.duplicate_detector = (
            DuplicateDetector(duplicate_key_fields) if duplicate_key_fields else None
        )
        self.geo_config = geo_config

    def validate_batch(
        self, records: list[dict[str, Any]]
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], ValidationReport]:
        """
        Validate a list of records.
        Returns (valid_records, rejected_records, report).
        """
        report = ValidationReport(total_records=len(records))
        valid: list[dict[str, Any]] = []
        rejected: list[dict[str, Any]] = []

        if self.duplicate_detector:
            self.duplicate_detector.reset()

        for i, record in enumerate(records):
            errors: list[dict[str, Any]] = []

            if self.duplicate_detector and self.duplicate_detector.is_duplicate(record):
                errors.append(
                    {
                        "record": i,
                        "field": str(self.duplicate_detector.key_fields),
                        "error": "DUPLICATE_RECORD",
                        "message": "Record is a duplicate based on key fields.",
                    }
                )

            errors.extend(self.validator.validate_record(record, i))

            if self.geo_config:
                lat_f, lon_f = self.geo_config
                errors.extend(
                    GeographicValidator.validate_lat_lon(record, lat_f, lon_f, i)
                )

            if errors:
                report.invalid_records += 1
                report.errors.extend(errors)
                rejected.append({"record": record, "errors": errors})
            else:
                report.valid_records += 1
                valid.append(record)

        return valid, rejected, report
