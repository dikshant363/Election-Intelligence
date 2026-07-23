"""ETL exception hierarchy."""


class ETLException(Exception):
    """Base exception for all ETL operations."""

    def __init__(self, message: str, code: str = "ETL_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class ConnectorError(ETLException):
    """Raised when a source connector fails to fetch data."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="CONNECTOR_ERROR")


class ParseError(ETLException):
    """Raised when a parser cannot process input data."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="PARSE_ERROR")


class ValidationError(ETLException):
    """Raised when record validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="VALIDATION_ERROR")


class TransformationError(ETLException):
    """Raised when a transformation fails to normalize a record."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="TRANSFORMATION_ERROR")


class LoadError(ETLException):
    """Raised when a loader fails to persist records to the database."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="LOAD_ERROR")


class DuplicateRecordError(ETLException):
    """Raised when a duplicate record is detected during import."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="DUPLICATE_RECORD")


class JobError(ETLException):
    """Raised when an import job encounters an unrecoverable failure."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="JOB_ERROR")
