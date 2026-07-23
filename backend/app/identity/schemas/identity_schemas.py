"""Pydantic v2 schemas for Identity and IAM API endpoints."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Payload for username/email & password authentication."""

    email: EmailStr = Field(..., example="admin@electionintelligence.org")
    password: str = Field(..., example="SecurePassword123!")


class TokenResponse(BaseModel):
    """Bearer JWT access and refresh token response."""

    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 1800


class RefreshTokenRequest(BaseModel):
    """Payload for requesting access token renewal."""

    refresh_token: str = Field(..., example="raw_refresh_token_string")


class UserCreateRequest(BaseModel):
    """Payload for user account creation."""

    email: EmailStr = Field(..., example="officer@electionintelligence.org")
    full_name: str = Field(..., min_length=2, max_length=150, example="Rajesh Sharma")
    password: str = Field(..., min_length=8, example="SecurePassword123!")
    roles: list[str] = Field(default_factory=lambda: ["PublicUser"])


class UserResponse(BaseModel):
    """Public API representation of User account."""

    id: str
    email: str
    full_name: str
    is_active: bool
    roles: list[str]
    created_at: datetime


class ApiKeyCreateRequest(BaseModel):
    """Payload for generating developer or service account API key."""

    name: str = Field(..., min_length=2, max_length=100, example="Analytics Pipeline Key")
    scopes: str = Field(default="elections:read,candidates:read", example="elections:read")


class ApiKeyCreatedResponse(BaseModel):
    """Response containing raw API key (only shown once at creation time)."""

    id: str
    name: str
    api_key: str
    key_prefix: str
    scopes: str
    created_at: datetime


class AuditEntryResponse(BaseModel):
    """Public representation of an immutable audit entry."""

    id: str
    user_id: str | None
    action: str
    resource: str
    ip_address: str | None
    details: str | None
    timestamp: datetime
