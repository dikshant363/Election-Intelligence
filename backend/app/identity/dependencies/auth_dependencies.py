"""FastAPI dependencies for authentication, role enforcement, and permission checks."""

from collections.abc import Callable
from dataclasses import dataclass, field

from fastapi import Request

from app.identity.exceptions import AuthenticationError, AuthorizationError
from app.identity.services import RbacService


@dataclass(frozen=True)
class CurrentUser:
    """Authenticated user context representation."""

    id: str
    roles: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    is_authenticated: bool = True


async def get_current_user(request: Request) -> CurrentUser:
    """FastAPI dependency extracting authenticated CurrentUser from request.state."""
    identity = getattr(request.state, "identity", None)
    if not identity or not identity.get("is_authenticated"):
        raise AuthenticationError("Authentication required.")
    return CurrentUser(
        id=identity["sub"],
        roles=identity.get("roles", []),
        permissions=identity.get("permissions", []),
        is_authenticated=True,
    )


def require_role(role_name: str) -> Callable[..., CurrentUser]:
    """Dependency factory enforcing that the authenticated user possesses a specified role."""

    async def role_checker(request: Request) -> CurrentUser:
        user = await get_current_user(request)
        if not RbacService.has_role(user.roles, role_name):
            raise AuthorizationError(
                f"Role '{role_name}' is required to access this resource."
            )
        return user

    return role_checker


def require_permission(permission_code: str) -> Callable[..., CurrentUser]:
    """Dependency factory enforcing that the authenticated user holds a specified permission."""

    async def permission_checker(request: Request) -> CurrentUser:
        user = await get_current_user(request)
        if not RbacService.has_permission(user.roles, permission_code):
            raise AuthorizationError(
                f"Permission '{permission_code}' is required to access this resource."
            )
        return user

    return permission_checker
