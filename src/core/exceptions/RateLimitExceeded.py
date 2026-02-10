from src.core.exceptions.BaseError import BaseError
from src.core.exceptions.enum import ErrorCode


class RateLimitExceeded(BaseError):
    """
    Exception raised when a client exceeds their credit limit.
    """

    def __init__(
        self,
        message="Rate limit exceeded.",
        original_exception=None,
        error_code=ErrorCode.RATE_LIMIT_EXCEEDED.value,
        status_code=429,
    ):
        super().__init__(message, original_exception, error_code, status_code)
        self.message = message
        self.original_exception = original_exception

    def __str__(self):
        return f"RateLimitExceeded: {self.message}"
