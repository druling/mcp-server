import logging

from src.core.exceptions.BaseError import BaseError
from src.servers import INTERNAL_MCP_SERVERS, INTEGRATION_MCP_SERVERS

logger = logging.getLogger(__name__)


class ToolService:
    async def all(self):
        """Get all tools"""
        try:
            return {
                "internal_tools": INTERNAL_MCP_SERVERS.keys(),
                "integration_tools": INTEGRATION_MCP_SERVERS.keys()
            }
        except Exception as e:
            raise BaseError(f"Error getting all tools: {e}")

    async def get_service_tools(self, tool_name):
        """Get tools for a specific service"""
        try:
            tool_service = None
            if tool_name in INTERNAL_MCP_SERVERS:
                tool_service = INTERNAL_MCP_SERVERS[tool_name]
            elif tool_name in INTEGRATION_MCP_SERVERS:
                tool_service = INTEGRATION_MCP_SERVERS[tool_name]

            tools = await tool_service.mcp.list_tools()
            return {
                "name": tool_name,
                "category": tool_service.category,
                "description": tool_service.description,
                "scope": tool_service.scope,
                "tools": tools
            }
        except Exception as e:
            raise BaseError(f"Error getting tools for service {tool_name}: {e}")
