"""Identity dependencies package initialization."""

from app.identity.dependencies.auth_dependencies import (
    CurrentUser,
    get_current_user,
    require_permission,
    require_role,
)

__all__ = [
    "CurrentUser",
    "get_current_user",
    "require_permission",
    "require_role",
]
