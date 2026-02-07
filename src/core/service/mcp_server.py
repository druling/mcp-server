import logging
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Optional

from mcp.server.fastmcp import FastMCP, Context
from mcp.types import Tool, Prompt
from starlette.requests import Request

from src.core.middleware import InternalAuth

logger = logging.getLogger(__name__)


@dataclass
class UserContext:
    """User context extracted from request headers."""
    user_id: str
    secret_id: str
    workspace_id: Optional[str] = None


@asynccontextmanager
async def extract_user_context(request: Request) -> AsyncIterator[UserContext]:
    """
    Extract user context from request headers.

    Headers expected:
    - X-User-ID: The user identifier
    - X-Secret-ID: The secret/auth identifier
    - X-Workspace-ID: Optional workspace identifier
    """
    user_id = request.headers.get("X-User-ID")
    secret_id = request.headers.get("X-Secret-ID")
    workspace_id = request.headers.get("X-Workspace-ID")

    if not user_id or not secret_id:
        raise ValueError("Missing required headers: X-User-ID and X-Secret-ID")

    logger.debug(f"User context: user_id={user_id}, workspace_id={workspace_id}")

    yield UserContext(
        user_id=user_id,
        secret_id=secret_id,
        workspace_id=workspace_id
    )


@dataclass
class BaseMCPServer(ABC):
    """
    Base MCP Server with common functionality.

    Provides:
    - FastMCP initialization
    - Internal token authentication
    - User/workspace context management via headers
    - Abstract methods for tool and prompt registration

    Headers expected from client:
    - X-User-ID: The user identifier
    - X-Secret-ID: The secret/auth identifier
    - X-Workspace-ID: Optional workspace identifier
    """

    name: str
    version: str = "1.0.0"
    internal_token: Optional[str] = None
    _mcp: FastMCP = field(init=False)
    _auth: InternalAuth = field(init=False)

    def __post_init__(self):
        """Initialize the MCP server and register handlers."""
        self._mcp = FastMCP(
            name=self.name,
            lifespan=extract_user_context
        )
        self._auth = InternalAuth(expected_token=self.internal_token)
        self._register_tools()
        self._register_prompts()
        logger.info(f"{self.__class__.__name__} initialized: {self.name} v{self.version}")

    @property
    def mcp(self) -> FastMCP:
        """Get the underlying FastMCP instance."""
        return self._mcp

    def get_user_context(self, ctx: Context) -> UserContext:
        """
        Get user context from MCP Context.

        Use this in tool handlers to access user_id, secret_id, workspace_id.

        Args:
            ctx: The MCP Context passed to tool handlers

        Returns:
            UserContext with user credentials
        """
        return ctx.request_context.lifespan_context

    def authenticate_internal(self, token: str) -> dict:
        """
        Authenticate using internal token.

        Args:
            token: The internal authentication token

        Returns:
            dict: Authentication result

        Raises:
            ValueError: If authentication fails
        """
        return self._auth.authenticate(token)


    @abstractmethod
    def _register_tools(self) -> None:
        """Register all tools with the MCP server. Must be implemented by subclasses."""
        pass

    def _register_prompts(self) -> None:
        """Register prompts with the MCP server. Override in subclasses if needed."""
        pass

    def get_tool_definitions(self) -> list[Tool]:
        """Get all tool definitions for this server. Override in subclasses."""
        return []

    def get_prompt_definitions(self) -> list[Prompt]:
        """Get all prompt definitions for this server. Override in subclasses."""
        return []
