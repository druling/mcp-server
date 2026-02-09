import traceback

from src.core.exceptions.enum import ErrorCode


class BaseError(Exception):
    def __init__(
        self,
        message,
        original_exception=None,
        error_code=ErrorCode.SERVER_ERROR.value,
        status_code=500,
    ):
        self.message = message
        self.original_exception = original_exception
        self.error_code = error_code
        self.status_code = status_code

        if original_exception:
            self.traceback = traceback.format_exception(
                type(original_exception),
                original_exception,
                original_exception.__traceback__,
            )
        else:
            self.traceback = None

        super().__init__(self.message)

    def __str__(self):
        if self.original_exception:
            return (
                f"{self.message}\n"
                f"Original Exception: {type(self.original_exception).__name__} - {str(self.original_exception)}\n"
                f"Traceback:\n{''.join(self.traceback)}"
            )
        return self.message

    def __repr__(self):
        if self.original_exception:
            return (
                f"<BaseError(message={self.message}, "
                f"original_exception={type(self.original_exception).__name__})>"
            )
        return f"<BaseError(message={self.message})>"
