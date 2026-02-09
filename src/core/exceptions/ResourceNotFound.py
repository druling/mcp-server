from src.core.exceptions.BaseError import BaseError
from src.core.exceptions.enum import ErrorCode


class ResourceNotFound(BaseError):
    """
    Exception raised when a requested resource is not found.
    """

    def __init__(
        self,
        message="This resource was not found.",
        original_exception=None,
        error_code=ErrorCode.RESOURCE_NOT_FOUND.value,
        status_code=404,
    ):
        super().__init__(message, original_exception, error_code, status_code)
        self.message = message
        self.original_exception = original_exception

    def __str__(self):
        return f"ResourceNotFound: {self.message}"
