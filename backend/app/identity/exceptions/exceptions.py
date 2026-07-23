"""Identity, authentication, and authorization exception classes."""


class IdentityException(Exception):
    """Base exception for IAM layer failures."""

    def __init__(self, message: str, code: str = "IDENTITY_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class AuthenticationError(IdentityException):
    """Exception raised when user credentials or authentication tokens are invalid."""

    def __init__(self, message: str = "Authentication failed.") -> None:
        super().__init__(message, code="UNAUTHORIZED")


class AuthorizationError(IdentityException):
    """Exception raised when user lacks required role or permission."""

    def __init__(self, message: str = "Permission denied.") -> None:
        super().__init__(message, code="FORBIDDEN")


class TokenExpiredError(AuthenticationError):
    """Exception raised when a JWT access or refresh token has expired."""

    def __init__(self, message: str = "Token has expired.") -> None:
        super().__init__(message)
        self.code = "TOKEN_EXPIRED"


class InvalidTokenError(AuthenticationError):
    """Exception raised when a token signature or claim is invalid."""

    def __init__(self, message: str = "Invalid token format or signature.") -> None:
        super().__init__(message)
        self.code = "INVALID_TOKEN"
