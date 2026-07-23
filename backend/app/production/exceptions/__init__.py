"""Production Hardening Layer exception hierarchy."""

from __future__ import annotations


class ProductionException(Exception):
    """Base exception for production hardening and security operations."""

    def __init__(self, message: str, code: str = "PRODUCTION_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class SecretsError(ProductionException):
    """Raised when secret retrieval or validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="SECRETS_ERROR")


class ConfigurationError(ProductionException):
    """Raised when startup configuration validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="CONFIGURATION_ERROR")


class BackupError(ProductionException):
    """Raised when database snapshot backup or recovery fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="BACKUP_ERROR")


class CircuitBreakerOpenError(ProductionException):
    """Raised when a request is rejected because the circuit breaker is OPEN."""

    def __init__(self, service_name: str) -> None:
        super().__init__(f"Circuit breaker for '{service_name}' is OPEN", code="CIRCUIT_OPEN_ERROR")
