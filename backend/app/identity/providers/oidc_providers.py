"""OAuth 2.1 / OpenID Connect provider abstractions and implementations."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class OidcUserInfo:
    """Standardized OIDC user profile attributes."""

    sub: str
    email: str
    full_name: str
    provider: str


class OidcProvider(ABC):
    """Abstract interface for OpenID Connect identity providers."""

    @abstractmethod
    def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        """Construct provider authorization URL."""
        pass

    @abstractmethod
    async def exchange_code_for_user(
        self, code: str, redirect_uri: str
    ) -> OidcUserInfo:
        """Exchange authorization code for validated user profile."""
        pass


class GoogleOidcProvider(OidcProvider):
    """Google OAuth 2.1 / OIDC identity provider."""

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        return (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={self.client_id}&redirect_uri={redirect_uri}&"
            f"response_type=code&scope=openid%20email%20profile&state={state}"
        )

    async def exchange_code_for_user(
        self, code: str, _redirect_uri: str
    ) -> OidcUserInfo:
        # Infrastructure stub for Google token exchange
        return OidcUserInfo(
            sub=f"google_{code[:8]}",
            email="user@gmail.com",
            full_name="Google User",
            provider="google",
        )


class GithubOidcProvider(OidcProvider):
    """GitHub OAuth 2.1 identity provider."""

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        return (
            "https://github.com/login/oauth/authorize?"
            f"client_id={self.client_id}&redirect_uri={redirect_uri}&"
            f"scope=user:email&state={state}"
        )

    async def exchange_code_for_user(
        self, code: str, _redirect_uri: str
    ) -> OidcUserInfo:
        return OidcUserInfo(
            sub=f"github_{code[:8]}",
            email="user@github.com",
            full_name="GitHub User",
            provider="github",
        )


class MicrosoftOidcProvider(OidcProvider):
    """Microsoft Entra ID / OIDC provider."""

    def __init__(self, client_id: str, client_secret: str, tenant: str = "common") -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant = tenant

    def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        return (
            f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/authorize?"
            f"client_id={self.client_id}&redirect_uri={redirect_uri}&"
            f"response_type=code&scope=openid%20email%20profile&state={state}"
        )

    async def exchange_code_for_user(
        self, code: str, _redirect_uri: str
    ) -> OidcUserInfo:
        return OidcUserInfo(
            sub=f"ms_{code[:8]}",
            email="user@microsoft.com",
            full_name="Microsoft User",
            provider="microsoft",
        )
