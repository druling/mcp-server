import logging
from contextvars import ContextVar
from typing import Optional

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from src.core.dtos.mcp_context import MCPContext
from src.core.enums.CustomHeader import CustomHeader

logger = logging.getLogger(__name__)

mcp_context_var: ContextVar[Optional[MCPContext]] = ContextVar("context", default=None)


class McpContextMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        user_id = headers.get(CustomHeader.X_PROFILE_ID.value.encode(), b"").decode() or None
        secret_id = headers.get(CustomHeader.X_SECRET_ID.value.encode(), b"").decode() or None
        entity_id = headers.get(CustomHeader.X_ENTITY_ID.value.encode(), b"").decode() or None
        entity_type = headers.get(CustomHeader.X_ENTITY_TYPE.value.encode(), b"").decode() or None

        if user_id:
            ctx = MCPContext(
                user_id=user_id,
                secret_id=secret_id,
                entity_id=entity_id,
                entity_type=entity_type,
            )
            token = mcp_context_var.set(ctx)
            try:
                await self.app(scope, receive, send)
            finally:
                mcp_context_var.reset(token)
        else:
            response = JSONResponse(
                status_code=400,
                content={"detail": "Missing required headers: X-Profile-ID"},
            )
            await response(scope, receive, send)


def get_mcp_context() -> MCPContext:
    ctx = mcp_context_var.get()
    if ctx is None:
        raise ValueError("Missing required headers: X-Profile-ID")
    return ctx
