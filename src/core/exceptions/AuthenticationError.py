from src.core.exceptions.BaseError import BaseError
from src.core.exceptions.enum import ErrorCode


class AuthenticationError(BaseError):
    """
    Exception raised for authentication failures.
    """

    def __init__(
        self,
        message="This action is not permitted.",
        original_exception=None,
        error_code=ErrorCode.AUTHENTICATION_ERROR.value,
        status_code=401,
    ):
        super().__init__(message, original_exception, error_code, status_code)
        self.message = message
        self.original_exception = original_exception

    def __str__(self):
        return f"AuthenticationError: {self.message}"
