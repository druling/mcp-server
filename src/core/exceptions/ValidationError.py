from src.core.exceptions.BaseError import BaseError
from src.core.exceptions.enum import ErrorCode


class ValidationError(BaseError):
    """
    Exception raised for validation errors.
    """

    def __init__(
        self,
        message="Validation error occurred.",
        original_exception=None,
        error_code=ErrorCode.VALIDATION_ERROR.value,
        status_code=400,
    ):
        super().__init__(message, original_exception, error_code, status_code)
        self.message = message
        self.original_exception = original_exception

    def __str__(self):
        return f"ValidationError: {self.message}"
