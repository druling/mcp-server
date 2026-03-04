import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.core.enums.CustomHeader import CustomHeader
from src.setup.config import config

logger = logging.getLogger(__name__)


class InternalAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.api_key = config.internal_secret
        self.excluded_paths = {"/health"}

    async def dispatch(self, request: Request, call_next):
        # Skip auth for excluded paths
        path = request.url.path.rstrip('/')
        if path not in self.excluded_paths:
            api_key = request.headers.get(CustomHeader.X_INTERNAL_AUTH.value)
            if api_key != self.api_key:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Unauthorized connection request"}
                )
                # return AuthenticationError("Unauthorized access")

        response = await call_next(request)
        return response
