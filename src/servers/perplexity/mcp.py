import logging
from dataclasses import dataclass

from src.clients.backend.client import BackendClient
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from . import outputs
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class PerplexityServer(BaseMCPServer):
    """MCP Server for Perplexity."""

    name: str = "perplexity"
    category: str = "Perplexity"
    description: str = "Perplexity integration for AI-powered search and research."
    scope: str = "perplexity_access_key"
    backend_service = BackendClient()
    base_url = "/perplexity"

    def _register_prompts(self) -> None:
        """Register all Perplexity prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Perplexity tools with the MCP server."""

        @self._mcp.tool(
            description="Reserve credits for Perplexity API usage.",
            meta=mcp_meta("reserve"),
            structured_output=True
        )
        async def reserve() -> outputs.ReserveResult:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/reserve/",
                data={},
                context=context
            )
            return outputs.ReserveResult(success=True, message="Credit reserved successfully")
