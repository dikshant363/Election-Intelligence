"""OIDC providers package initialization."""

from app.identity.providers.oidc_providers import (
    GithubOidcProvider,
    GoogleOidcProvider,
    MicrosoftOidcProvider,
    OidcProvider,
    OidcUserInfo,
)

__all__ = [
    "GithubOidcProvider",
    "GoogleOidcProvider",
    "MicrosoftOidcProvider",
    "OidcProvider",
    "OidcUserInfo",
]
