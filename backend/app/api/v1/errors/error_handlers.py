"""RFC 7807 Problem Details error handler and DomainError HTTP mapping."""

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.core.result import DomainError, ErrorCode, Result


class ProblemDetails(BaseModel):
    """RFC 7807 Problem Details schema."""

    type: str = Field(
        default="about:blank",
        example="https://api.electionintelligence.org/errors/validation-error",
    )
    title: str = Field(..., example="Validation Error")
    status: int = Field(..., example=422)
    detail: str = Field(..., example="Field 'title' cannot be empty.")
    instance: str = Field(..., example="/api/v1/elections")
    code: str = Field(..., example="VALIDATION_ERROR")


class ApiException(Exception):
    """API exception carrying RFC 7807 ProblemDetails."""

    def __init__(self, problem: ProblemDetails) -> None:
        super().__init__(problem.detail)
        self.problem = problem


def domain_error_to_status_code(error_code: ErrorCode) -> int:
    """Map domain ErrorCode to standard HTTP status code."""
    mapping = {
        ErrorCode.NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ErrorCode.CONFLICT: status.HTTP_409_CONFLICT,
        ErrorCode.VALIDATION_ERROR: status.HTTP_422_UNPROCESSABLE_ENTITY,
        ErrorCode.UNAUTHORIZED: status.HTTP_401_UNAUTHORIZED,
        ErrorCode.FORBIDDEN: status.HTTP_403_FORBIDDEN,
        ErrorCode.INTERNAL_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }
    return mapping.get(error_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


def raise_result_failure(result: Result[Any], request_path: str) -> None:
    """Transform failed Result into an ApiException carrying RFC 7807 problem details."""
    err: DomainError = result.error
    http_status = domain_error_to_status_code(err.code)
    problem = ProblemDetails(
        type=f"https://api.electionintelligence.org/errors/{err.code.value.lower()}",
        title=err.code.value.replace("_", " ").title(),
        status=http_status,
        detail=err.message,
        instance=request_path,
        code=err.code.value,
    )
    raise ApiException(problem)


def register_error_handlers(app: FastAPI) -> None:
    """Register RFC 7807 global exception handlers on FastAPI application."""

    @app.exception_handler(ApiException)
    async def api_exception_handler(
        request: Request, exc: ApiException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.problem.status,
            content=exc.problem.model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        details_list = [
            f"{' -> '.join(str(loc) for loc in err['loc'])}: {err['msg']}"
            for err in exc.errors()
        ]
        problem = ProblemDetails(
            type="https://api.electionintelligence.org/errors/request-validation",
            title="Unprocessable Entity",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="; ".join(details_list),
            instance=request.url.path,
            code="REQUEST_VALIDATION_ERROR",
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=problem.model_dump(),
        )
