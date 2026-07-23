"""API v1 errors package initialization."""

from app.api.v1.errors.error_handlers import (
    ApiException,
    ProblemDetails,
    domain_error_to_status_code,
    raise_result_failure,
    register_error_handlers,
)

__all__ = [
    "ApiException",
    "ProblemDetails",
    "domain_error_to_status_code",
    "register_error_handlers",
    "raise_result_failure",
]
