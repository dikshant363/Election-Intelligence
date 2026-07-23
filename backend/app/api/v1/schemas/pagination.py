"""Generic pagination request and response schemas."""

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Query parameters for pagination."""

    page: int = Field(default=1, ge=1, description="Page number starting from 1")
    size: int = Field(
        default=20, ge=1, le=100, description="Items per page (max 100)"
    )

    @property
    def skip(self) -> int:
        """Calculate offset count."""
        return (self.page - 1) * self.size


class PaginatedResponse[T](BaseModel):
    """Generic paginated response wrapper."""

    items: list[T]
    total: int
    page: int
    size: int
    pages: int
