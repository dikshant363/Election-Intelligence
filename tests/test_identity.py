"""Unit and integration tests for Identity, IAM, Authentication, and Authorization."""

from datetime import timedelta

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.api.v1.dependencies import get_uow
from app.config import settings
from app.database.base import Base
from app.identity.dependencies import (
    get_current_user,
    require_role,
)
from app.identity.exceptions import (
    AuthenticationError,
    AuthorizationError,
    InvalidTokenError,
    TokenExpiredError,
)
from app.identity.providers import (
    GithubOidcProvider,
    GoogleOidcProvider,
    MicrosoftOidcProvider,
)
from app.identity.services import (
    ApiKeyService,
    JwtService,
    PasswordService,
    RbacService,
    RoleHierarchy,
)
from app.main import app
from app.persistence.uow import SqlAlchemyUnitOfWork, UnitOfWork


@pytest_asyncio.fixture
async def test_session_factory() -> async_sessionmaker[AsyncSession]:
    """Provide NullPool AsyncEngine & session factory for identity testing."""
    test_engine = create_async_engine(
        settings.DATABASE_URL,
        poolclass=NullPool,
    )
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    yield session_factory
    await test_engine.dispose()


def test_argon2id_password_hashing_and_verification() -> None:
    """Verify PasswordService Argon2id hashing, legacy PBKDF2 verification, and rehash detection."""
    raw_pw = "SecureP@ssword123!"
    hashed = PasswordService.hash_password(raw_pw)
    assert hashed.startswith("$argon2id$")
    assert PasswordService.verify_password(raw_pw, hashed) is True
    assert PasswordService.verify_password("WrongPassword!", hashed) is False
    assert PasswordService.needs_rehash(hashed) is False

    # Legacy PBKDF2 hash verification & rehash migration test
    legacy_hash = "pbkdf2_sha256$100000$c2FsdHNhbHRzYWx0c2FsdA==$S2V5S2V5S2V5S2V5S2V5S2V5S2V5S2V5S2V5S2V5S2V5"
    assert PasswordService.needs_rehash(legacy_hash) is True

    # Password policy
    weak_pw = "weak"
    violations = PasswordService.validate_password_strength(weak_pw)
    assert len(violations) > 0
    assert any("at least 8 characters" in v for v in violations)


def test_jwt_token_lifecycle() -> None:
    """Verify JwtService access token creation, HMAC verification, and expiration."""
    user_id = "11111111-2222-3333-4444-555555555555"
    roles = ["ElectionCommissioner"]
    permissions = ["elections:create"]

    token = JwtService.create_access_token(
        subject=user_id,
        roles=roles,
        permissions=permissions,
        expires_delta=timedelta(minutes=15),
    )
    payload = JwtService.decode_and_verify_token(token)
    assert payload["sub"] == user_id
    assert payload["roles"] == roles
    assert payload["permissions"] == permissions

    # Test expired token
    expired_token = JwtService.create_access_token(
        subject=user_id,
        roles=roles,
        permissions=permissions,
        expires_delta=timedelta(seconds=-120),  # Expired 2 minutes ago
    )
    with pytest.raises(TokenExpiredError):
        JwtService.decode_and_verify_token(expired_token)

    # Test tampered token
    tampered_token = token[:-5] + "XXXXX"
    with pytest.raises(InvalidTokenError):
        JwtService.decode_and_verify_token(tampered_token)


def test_rbac_permission_evaluation() -> None:
    """Verify RbacService role hierarchy and permission checking."""
    # PlatformAdmin has wildcard permission
    admin_perms = RbacService.get_permissions_for_roles([RoleHierarchy.PLATFORM_ADMIN])
    assert "*" in admin_perms
    assert RbacService.has_permission([RoleHierarchy.PLATFORM_ADMIN], "any:permission") is True

    # ElectionCommissioner permissions
    comm_perms = RbacService.get_permissions_for_roles([RoleHierarchy.ELECTION_COMMISSIONER])
    assert "elections:create" in comm_perms
    assert "results:declare" in comm_perms
    assert RbacService.has_permission([RoleHierarchy.ELECTION_COMMISSIONER], "elections:create") is True

    # Analyst permissions (read-only)
    analyst_perms = RbacService.get_permissions_for_roles([RoleHierarchy.ANALYST])
    assert "elections:read" in analyst_perms
    assert RbacService.has_permission([RoleHierarchy.ANALYST], "elections:create") is False


def test_api_key_service() -> None:
    """Verify ApiKeyService generation, hashing, and scope validation."""
    raw_key, prefix, key_hash = ApiKeyService.generate_api_key()
    assert raw_key.startswith("ei_live_")
    assert prefix == raw_key[:16]
    assert ApiKeyService.verify_key(raw_key, key_hash) is True
    assert ApiKeyService.verify_key("ei_live_invalid_key_string", key_hash) is False

    scopes = "elections:read,candidates:read"
    assert ApiKeyService.has_scope(scopes, "elections:read") is True
    assert ApiKeyService.has_scope(scopes, "results:declare") is False


def test_oidc_providers_url_generation() -> None:
    """Verify OIDC provider authorization URL generation."""
    google = GoogleOidcProvider(client_id="g_client", client_secret="g_secret")
    url_g = google.get_authorization_url(state="xyz", redirect_uri="http://localhost/callback")
    assert "accounts.google.com" in url_g
    assert "g_client" in url_g

    github = GithubOidcProvider(client_id="gh_client", client_secret="gh_secret")
    url_gh = github.get_authorization_url(state="xyz", redirect_uri="http://localhost/callback")
    assert "github.com/login/oauth/authorize" in url_gh

    ms = MicrosoftOidcProvider(client_id="ms_client", client_secret="ms_secret")
    url_ms = ms.get_authorization_url(state="xyz", redirect_uri="http://localhost/callback")
    assert "login.microsoftonline.com" in url_ms


@pytest.mark.asyncio
async def test_protected_endpoints_with_identity_middleware(
    test_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """Verify FastAPI identity middleware & auth dependencies on protected route simulation."""

    async def override_get_uow() -> UnitOfWork:
        uow = SqlAlchemyUnitOfWork(session_factory=test_session_factory)
        yield uow

    app.dependency_overrides[get_uow] = override_get_uow

    token = JwtService.create_access_token(
        subject="user-123",
        roles=["PlatformAdmin"],
        permissions=["*"],
    )
    headers = {"Authorization": f"Bearer {token}"}

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        res = await client.get("/api/v1/elections", headers=headers)
        assert res.status_code == 200

    app.dependency_overrides.clear()

    # Test unauthenticated request to protected dependency
    class MockRequest:
        state = type("State", (), {"identity": {"is_authenticated": False}})()

    with pytest.raises(AuthenticationError):
        await get_current_user(MockRequest())

    # Test forbidden role request
    class MockUserRequest:
        state = type(
            "State",
            (),
            {
                "identity": {
                    "is_authenticated": True,
                    "sub": "user-456",
                    "roles": ["PublicUser"],
                }
            },
        )()

    role_dep = require_role("ElectionCommissioner")
    with pytest.raises(AuthorizationError):
        await role_dep(MockUserRequest())
