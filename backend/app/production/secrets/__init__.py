"""Secrets Management Provider abstraction, EnvSecretsProvider, and Vault/Cloud adapter hooks."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod

from app.production.exceptions import SecretsError


class SecretsProvider(ABC):
    """Abstract secrets manager provider."""

    @abstractmethod
    def get_secret(self, key: str, default: str | None = None) -> str:
        pass

    @abstractmethod
    def validate_secrets(self, required_keys: list[str]) -> list[str]:
        pass


class EnvSecretsProvider(SecretsProvider):
    """Environment variable-backed secrets provider."""

    def get_secret(self, key: str, default: str | None = None) -> str:
        val = os.getenv(key, default)
        if val is None:
            raise SecretsError(f"Secret '{key}' not found in environment variables")
        return val

    def validate_secrets(self, required_keys: list[str]) -> list[str]:
        return [k for k in required_keys if not os.getenv(k)]


class VaultSecretsAdapter(SecretsProvider):
    """HashiCorp Vault secrets manager adapter hook."""

    def __init__(self, fallback: EnvSecretsProvider | None = None) -> None:
        self._fallback = fallback or EnvSecretsProvider()

    def get_secret(self, key: str, default: str | None = None) -> str:
        return self._fallback.get_secret(key, default)

    def validate_secrets(self, required_keys: list[str]) -> list[str]:
        return self._fallback.validate_secrets(required_keys)


class CloudSecretManagerAdapter(SecretsProvider):
    """AWS Secrets Manager / GCP Secret Manager adapter hook."""

    def __init__(self, fallback: EnvSecretsProvider | None = None) -> None:
        self._fallback = fallback or EnvSecretsProvider()

    def get_secret(self, key: str, default: str | None = None) -> str:
        return self._fallback.get_secret(key, default)

    def validate_secrets(self, required_keys: list[str]) -> list[str]:
        return self._fallback.validate_secrets(required_keys)


# Global secrets provider
global_secrets_provider = EnvSecretsProvider()
