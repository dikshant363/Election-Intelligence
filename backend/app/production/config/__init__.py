"""Startup configuration validation and SHA-256 fingerprinting."""

from __future__ import annotations

import hashlib

from app.config import settings
from app.production.schemas import ConfigValidationSchema


class ConfigurationValidator:
    """Validates application environment settings on startup."""

    REQUIRED_KEYS = ["PROJECT_NAME", "VERSION", "ENVIRONMENT"]

    @classmethod
    def validate_configuration(cls) -> ConfigValidationSchema:
        missing = []
        for k in cls.REQUIRED_KEYS:
            if not getattr(settings, k, None):
                missing.append(k)

        invalid = []
        if settings.ENVIRONMENT not in ["development", "testing", "staging", "production"]:
            invalid.append("ENVIRONMENT")

        # Generate configuration fingerprint
        fingerprint_raw = f"{settings.PROJECT_NAME}:{settings.VERSION}:{settings.ENVIRONMENT}"
        fingerprint = hashlib.sha256(fingerprint_raw.encode("utf-8")).hexdigest()[:16]

        status = "invalid" if missing or invalid else "valid"

        return ConfigValidationSchema(
            status=status,
            environment=settings.ENVIRONMENT,
            fingerprint=fingerprint,
            missing_keys=missing,
            invalid_keys=invalid,
        )
