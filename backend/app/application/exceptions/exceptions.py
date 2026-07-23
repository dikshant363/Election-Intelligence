"""Application layer exception definitions."""


class ApplicationException(Exception):
    """Base application layer exception."""

    def __init__(self, message: str, code: str = "APPLICATION_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class CommandValidationError(ApplicationException):
    """Exception raised when command parameter validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="VALIDATION_ERROR")


class EntityNotFoundError(ApplicationException):
    """Exception raised when target entity does not exist."""

    def __init__(self, entity_name: str, entity_id: str) -> None:
        super().__init__(
            f"{entity_name} with ID '{entity_id}' not found.",
            code="NOT_FOUND",
        )
