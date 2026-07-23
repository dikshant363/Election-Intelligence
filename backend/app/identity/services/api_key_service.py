"""API Key service for service accounts and developer API access."""

import hashlib
import secrets


class ApiKeyService:
    """Service providing secure API key generation, hashing, and scope validation."""

    PREFIX = "ei_live_"
    PREFIX_LENGTH = 16

    @classmethod
    def generate_api_key(cls) -> tuple[str, str, str]:
        """Generate API key. Returns (raw_key, key_prefix, key_hash)."""
        random_part = secrets.token_urlsafe(32)
        raw_key = f"{cls.PREFIX}{random_part}"
        key_prefix = raw_key[: cls.PREFIX_LENGTH]
        key_hash = cls.hash_key(raw_key)
        return raw_key, key_prefix, key_hash

    @classmethod
    def hash_key(cls, raw_key: str) -> str:
        """Hash raw API key using SHA-256."""
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    @classmethod
    def verify_key(cls, raw_key: str, stored_hash: str) -> bool:
        """Verify raw key against stored hash using constant time comparison."""
        candidate_hash = cls.hash_key(raw_key)
        return secrets.compare_digest(candidate_hash, stored_hash)

    @classmethod
    def has_scope(cls, key_scopes: str, required_scope: str) -> bool:
        """Check if API key scopes include required scope."""
        scopes_list = [s.strip() for s in key_scopes.split(",")]
        return "*" in scopes_list or required_scope in scopes_list
