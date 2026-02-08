import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.setup.config import config

logger = logging.getLogger(__name__)


class InternalAuthMiddleware(BaseHTTPMiddleware):
    """Middleware to validate internal auth token from headers."""

    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("X-INTERNAL-AUTH")

        if token is None or token != config.internal_secret:
            logger.warning(f"Unauthorized request from {request.client.host if request.client else 'unknown'}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized connection request"}
            )

        return await call_next(request)
