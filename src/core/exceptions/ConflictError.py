from src.core.exceptions.BaseError import BaseError
from src.core.exceptions.enum import ErrorCode


class ConflictError(BaseError):
    """
    Exception raised for conflict errors.
    """

    def __init__(
        self,
        message="This action would cause a conflict.",
        original_exception=None,
        error_code=ErrorCode.CONFLICT_ERROR.value,
        status_code=409,
    ):
        super().__init__(message, original_exception, error_code, status_code)
        self.message = message
        self.original_exception = original_exception

    def __str__(self):
        return f"ConflictError: {self.message}"
