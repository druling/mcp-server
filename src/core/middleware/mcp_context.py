import logging
from _contextvars import ContextVar
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.core.dtos.mcp_context import MCPContext

logger = logging.getLogger(__name__)

mcp_context_var: ContextVar[Optional[MCPContext]] = ContextVar("context", default=None)

class McpContextMiddleware(BaseHTTPMiddleware):
    """Middleware to extract user context from headers and store in context var."""

    async def dispatch(self, request: Request, call_next):
        user_id = request.headers.get("X-PROFILE-ID")
        secret_id = request.headers.get("X-SECRET-ID")
        entity_id = request.headers.get("X-ENTITY-ID")
        entity_type = request.headers.get("X-ENTITY-TYPE")

        if user_id:
            user_ctx = MCPContext(
                user_id=user_id,
                secret_id=secret_id,
                entity_id=entity_id,
                entity_type=entity_type,
            )
            token = mcp_context_var.set(user_ctx)
            try:
                response = await call_next(request)
                return response
            finally:
                mcp_context_var.reset(token)
        else:
            return JSONResponse(
                status_code=400,
                content={"detail": "Missing required headers: X-Profile-ID"}
            )


def get_mcp_context() -> MCPContext:
    """Get the current user context from context var."""
    ctx = mcp_context_var.get()
    if ctx is None:
        raise ValueError("Missing required headers: X-Profile-ID")
    return ctx
