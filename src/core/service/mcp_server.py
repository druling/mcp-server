import logging
from dataclasses import field

from mcp.server import FastMCP

logger = logging.getLogger(__name__)


class MCPServer:
    _mcp: FastMCP = field(init=False)

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    @property
    def mcp(self) -> FastMCP:
        """Get the underlying FastMCP instance."""
        return self._mcp

    def get_server_info(self) -> dict:
        """
        Get server information.

        Returns:
            dict: Server information including name, version, and capabilities
        """
        return {
            "name": self.name,
            "version": self.version,
            "initialized": self._initialized,
            "user_id": self.user_id,
            "workspace_id": self.workspace_id,
            "capabilities": {
                "tools": len(self.get_tool_definitions()),
                "prompts": len(self.get_prompt_definitions()),
            }
        }

    async def run(self, transport: str = "stdio") -> None:
        """
        Run the MCP server.

        Args:
            transport: Transport type (stdio, sse, etc.)
        """
        logger.info(f"Starting {self.name} server with {transport} transport")
        await self._mcp.run(transport=transport)