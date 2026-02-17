import logging

from src.core.exceptions.BaseError import BaseError
from src.setup.mcp import INTERNAL_MCP_PATH, INTEGRATION_MCP_PATH

logger = logging.getLogger(__name__)


class ToolService:
    async def all(self):
        """Get all tools"""
        try:
            return {
                "internal_tools": [INTERNAL_MCP_PATH.keys()],
                "integration_tools": [INTEGRATION_MCP_PATH.keys()]
            }
        except Exception as e:
            raise BaseError(f"Error getting all tools: {e}")

    async def get_service_tools(self, tool_name):
        """Get tools for a specific service"""
        try:
            tool_service = None
            if tool_name in INTERNAL_MCP_PATH:
                tool_service = INTERNAL_MCP_PATH[tool_name]
            elif tool_name in INTEGRATION_MCP_PATH:
                tool_service = INTEGRATION_MCP_PATH[tool_name]
            return {
                "tool_name": tool_name,
                "service": tool_service.mcp.instructions
            }
        except Exception as e:
            raise BaseError(f"Error getting tools for service {tool_name}: {e}")
