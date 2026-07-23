"""Identity context middleware setting user state and correlation ID on incoming HTTP requests."""

from collections.abc import Awaitable, Callable
from typing import Any

from starlette.requests import Request
from starlette.responses import Response

from app.identity.services import JwtService


async def identity_context_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Middleware extracting Bearer tokens and attaching user identity context to request.state."""
    auth_header = request.headers.get("Authorization")
    user_context: dict[str, Any] = {
        "is_authenticated": False,
        "sub": None,
        "roles": [],
        "permissions": [],
    }

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = JwtService.decode_and_verify_token(token)
            user_context = {
                "is_authenticated": True,
                "sub": payload.get("sub"),
                "roles": payload.get("roles", []),
                "permissions": payload.get("permissions", []),
            }
        except Exception:
            pass

    request.state.identity = user_context
    return await call_next(request)
