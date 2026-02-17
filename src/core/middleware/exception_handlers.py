import logging

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Any, Dict

from src.core.api.responses import ResponseFactory
from src.core.exceptions import BaseError

logger = logging.getLogger(__name__)


class ExceptionHandlers:
    """Class to organize exception handling logic"""

    @staticmethod
    def get_request_context(request: Request) -> Dict[str, Any]:
        """Extract common request context for logging"""
        return {
            "method": request.method,
            "url": str(request.url),
        }


    @classmethod
    async def handle_base_error(cls, request: Request, exc: BaseError) -> JSONResponse:
        """Handle unhandled exceptions"""
        context = cls.get_request_context(request)

        logger.error(
            f"Error: {exc.message}",
            extra=context,
            exc_info=True
        )

        return ResponseFactory.error(message=exc.message, status_code=exc.status_code, error_code=exc.error_code, errors=str(exc))

    @classmethod
    async def handle_global_exception(cls, request: Request, exc: Exception) -> JSONResponse:
        """Handle unhandled exceptions"""
        context = cls.get_request_context(request)

        logger.error(
            f"Unhandled exception: {exc}",
            extra=context,
            exc_info=True
        )

        return ResponseFactory.error(message="Internal server error")

    @classmethod
    async def handle_http_exception(cls, request: Request, exc: HTTPException) -> JSONResponse:
        """Handle HTTP exceptions"""
        context = cls.get_request_context(request)
        context["status_code"] = exc.status_code

        logger.warning(
            f"HTTP {exc.status_code}: {exc.detail}",
            extra=context
        )
        return ResponseFactory.response(status_code=exc.status_code, data=exc.detail, message=exc.detail)
