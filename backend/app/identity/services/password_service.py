"""Password security service using PBKDF2/Argon2id hashing and password policy validation."""

import base64
import hashlib
import os
import secrets
import string

MIN_PASSWORD_LENGTH = 8


class PasswordService:
    """Service providing secure password hashing, verification, and policy enforcement."""

    ITERATIONS = 100_000
    SALT_SIZE = 16

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash a password using PBKDF2-HMAC-SHA256 with a random salt."""
        salt = os.urandom(cls.SALT_SIZE)
        key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            cls.ITERATIONS,
        )
        salt_b64 = base64.b64encode(salt).decode("ascii")
        key_b64 = base64.b64encode(key).decode("ascii")
        return f"pbkdf2_sha256${cls.ITERATIONS}${salt_b64}${key_b64}"

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        """Verify password against stored hash string."""
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
