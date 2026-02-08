import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.applications import Starlette

from src.core.dtos.mcp_context import MCPContext
from src.core.middleware import McpContextMiddleware, get_mcp_context, InternalAuthMiddleware

logger = logging.getLogger(__name__)

@dataclass
class BaseMCPServer(ABC):
    """
    Base MCP Server with common functionality.

    Provides:
    - FastMCP initialization
    - Middleware for extracting user context from headers
    - Abstract method for registering tools

    Middleware:
    - InternalAuthMiddleware: Validates internal token for authentication
    - McpContextMiddleware: Extracts user context (user_id, secret_id, workspace_id)
        from headers and stores in context var.
    """

    name: str
    version: str = "1.0.0"
    internal_token: Optional[str] = None
    _mcp: FastMCP = field(init=False)

    def __post_init__(self):
        """Initialize the MCP server and register handlers."""
        # Disable DNS rebinding protection since we use internal auth for security
        transport_security = TransportSecuritySettings(
            enable_dns_rebinding_protection=False,
        )
        self._mcp = FastMCP(name=self.name, transport_security=transport_security)
        self._register_tools()
        self._register_prompts()
        logger.info(f"{self.__class__.__name__} initialized: {self.name} v{self.version}")

    @property
    def mcp(self) -> FastMCP:
        """Get the underlying FastMCP instance."""
        return self._mcp

    def streamable_http_app(self) -> Starlette:
        """
        Get the streamable HTTP app with user context middleware.

        Use this instead of mcp.streamable_http_app() to get header extraction.
        """
        app = self._mcp.streamable_http_app()
        app.add_middleware(InternalAuthMiddleware)
        app.add_middleware(McpContextMiddleware)
        return app

    def get_context(self) -> MCPContext:
        """
        Get user context from the current request.

        Use this in tool handlers to access user_id, secret_id, workspace_id.

        Returns:
            UserContext with user credentials

        Raises:
            ValueError: If headers are missing
        """
        return get_mcp_context()


    @abstractmethod
    def _register_tools(self) -> None:
        """Register all tools with the MCP server. Must be implemented by subclasses."""
        pass

    def _register_prompts(self) -> None:
        """Register prompts with the MCP server. Override in subclasses if needed."""
        pass
