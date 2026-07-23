"""Password security service using Argon2id hashing, legacy PBKDF2 verification, and rehash migration."""

import base64
import hashlib
import secrets
import string

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

MIN_PASSWORD_LENGTH = 8


class PasswordService:
    """Service providing Argon2id password hashing, legacy PBKDF2 compatibility, and rehash migration."""

    _ph = PasswordHasher()  # Uses Argon2id default

    # Legacy PBKDF2 constants
    ITERATIONS = 100_000
    SALT_SIZE = 16

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash a password using modern Argon2id."""
        return cls._ph.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        """Verify password against Argon2id or legacy PBKDF2 hash."""
        if hashed_password.startswith("$argon2"):
            try:
                return cls._ph.verify(hashed_password, password)
            except (VerifyMismatchError, InvalidHashError, VerificationError):
                return False

        if hashed_password.startswith("pbkdf2_sha256$"):
            try:
                algorithm, iterations_str, salt_b64, key_b64 = hashed_password.split("$")
                if algorithm != "pbkdf2_sha256":
                    return False
                iterations = int(iterations_str)
                salt = base64.b64decode(salt_b64.encode("ascii"))
                expected_key = base64.b64decode(key_b64.encode("ascii"))
                candidate_key = hashlib.pbkdf2_hmac(
                    "sha256",
                    password.encode("utf-8"),
                    salt,
                    iterations,
                )
                return secrets.compare_digest(candidate_key, expected_key)
            except Exception:
                return False

        return False

    @classmethod
    def needs_rehash(cls, hashed_password: str) -> bool:
        """Check if stored hash needs transparent migration to current Argon2id parameters."""
        if not hashed_password.startswith("$argon2"):
            return True
        try:
            return cls._ph.check_needs_rehash(hashed_password)
        except Exception:
            return True

    @classmethod
    def validate_password_strength(cls, password: str) -> list[str]:
        """Validate password against security policy. Returns list of violation messages."""
        violations: list[str] = []
        if len(password) < MIN_PASSWORD_LENGTH:
            violations.append("Password must be at least 8 characters long.")
        if not any(c.isupper() for c in password):
            violations.append("Password must contain at least one uppercase letter.")
        if not any(c.islower() for c in password):
            violations.append("Password must contain at least one lowercase letter.")
        if not any(c.isdigit() for c in password):
            violations.append("Password must contain at least one digit.")
        if not any(c in string.punctuation for c in password):
            violations.append("Password must contain at least one special character.")
        return violations

    @classmethod
    def generate_reset_token(cls) -> str:
        """Generate a cryptographically secure password reset token."""
        return secrets.token_urlsafe(32)
