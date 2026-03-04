import logging

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from src.core.enums.CustomHeader import CustomHeader
from src.setup.config import config

logger = logging.getLogger(__name__)


class InternalAuthMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app
        self.api_key = config.internal_secret
        self.excluded_paths = {"/health"}

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope["path"].rstrip("/")
        if path not in self.excluded_paths:
            headers = dict(scope.get("headers", []))
            api_key = headers.get(CustomHeader.X_INTERNAL_AUTH.value.encode(), b"").decode()
            if api_key != self.api_key:
                response = JSONResponse(
                    status_code=401,
                    content={"detail": "Unauthorized connection request"},
                )
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)
