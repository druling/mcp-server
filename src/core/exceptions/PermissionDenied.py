from src.core.exceptions.BaseError import BaseError
from src.core.exceptions.enum import ErrorCode


class PermissionDenied(BaseError):
    """
    Exception raised for permission denied errors.
    """

    def __init__(
        self,
        message="This action is not permitted.",
        original_exception=None,
        error_code=ErrorCode.PERMISSION_DENIED.value,
        status_code=403,
    ):
        super().__init__(message, original_exception, error_code, status_code)
        self.message = message
        self.original_exception = original_exception

    def __str__(self):
        return f"PermissionDenied: {self.message}"
