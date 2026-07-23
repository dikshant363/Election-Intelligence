"""JWT Authentication service handling access/refresh tokens, signing, and verification."""

import base64
import hashlib
import hmac
import json
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from app.identity.exceptions import (
    AuthenticationError,
    InvalidTokenError,
    TokenExpiredError,
)

JWT_PARTS_COUNT = 3


class JwtService:
    """Service providing JWT encoding, decoding, signing, and claim verification."""

    SECRET_KEY = "election-intelligence-secret-key-change-in-prod"
    ISSUER = "election-intelligence-platform"
    AUDIENCE = "election-intelligence-api"
    CLOCK_SKEW_TOLERANCE_SECONDS = 60

    @classmethod
    def _base64url_encode(cls, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

    @classmethod
    def _base64url_decode(cls, data_str: str) -> bytes:
        padding = "=" * (4 - (len(data_str) % 4))
        return base64.urlsafe_b64decode((data_str + padding).encode("ascii"))

    @classmethod
    def create_access_token(
        cls,
        subject: str,
        roles: list[str],
        permissions: list[str],
        expires_delta: timedelta = timedelta(minutes=30),
    ) -> str:
        """Create signed JWT access token with user ID, roles, and permissions."""
        now = datetime.now(UTC)
        payload = {
            "sub": subject,
            "roles": roles,
            "permissions": permissions,
            "type": "access",
            "iss": cls.ISSUER,
            "aud": cls.AUDIENCE,
            "iat": int(now.timestamp()),
            "exp": int((now + expires_delta).timestamp()),
            "jti": str(uuid.uuid4()),
        }
        return cls._encode_jwt(payload)

    @classmethod
    def create_refresh_token(
        cls,
        subject: str,
        expires_delta: timedelta = timedelta(days=7),
    ) -> tuple[str, str, datetime]:
        """Create refresh token. Returns (raw_token, token_hash, expires_at)."""
        now = datetime.now(UTC)
        expires_at = now + expires_delta
        payload = {
            "sub": subject,
            "type": "refresh",
            "iss": cls.ISSUER,
            "aud": cls.AUDIENCE,
            "iat": int(now.timestamp()),
            "exp": int(expires_at.timestamp()),
            "jti": str(uuid.uuid4()),
        }
        raw_token = cls._encode_jwt(payload)
        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
        return raw_token, token_hash, expires_at

    @classmethod
    def _encode_jwt(cls, payload: dict[str, Any]) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        header_json = json.dumps(header, separators=(",", ":")).encode("utf-8")
        payload_json = json.dumps(payload, separators=(",", ":")).encode("utf-8")

        encoded_header = cls._base64url_encode(header_json)
        encoded_payload = cls._base64url_encode(payload_json)

        signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
        signature = hmac.new(
            cls.SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256
        ).digest()
        encoded_signature = cls._base64url_encode(signature)

        return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

    @classmethod
    def decode_and_verify_token(cls, token: str) -> dict[str, Any]:
        """Verify token signature, issuer, audience, and expiration."""
        try:
            parts = token.split(".")
            if len(parts) != JWT_PARTS_COUNT:
                raise InvalidTokenError("JWT token must consist of 3 parts.")

            encoded_header, encoded_payload, encoded_signature = parts

            # Verify signature
            signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
            expected_signature = hmac.new(
                cls.SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256
            ).digest()
            candidate_signature = cls._base64url_decode(encoded_signature)

            if not hmac.compare_digest(candidate_signature, expected_signature):
                raise InvalidTokenError("JWT signature verification failed.")

            payload_bytes = cls._base64url_decode(encoded_payload)
            payload = json.loads(payload_bytes.decode("utf-8"))

            # Verify claims
            now = int(datetime.now(UTC).timestamp())
            exp = payload.get("exp", 0)
            if now > exp + cls.CLOCK_SKEW_TOLERANCE_SECONDS:
                raise TokenExpiredError()

            if payload.get("iss") != cls.ISSUER:
                raise InvalidTokenError(f"Invalid token issuer: {payload.get('iss')}")

            if payload.get("aud") != cls.AUDIENCE:
                raise InvalidTokenError(f"Invalid token audience: {payload.get('aud')}")

            return payload
        except AuthenticationError:
            raise
        except Exception as err:
            raise InvalidTokenError(str(err)) from err
