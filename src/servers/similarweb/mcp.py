import json
import logging
from typing import Annotated
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import IntegrationAppClient
from src.core.outputs import mcp_output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class SimilarwebServer(BaseMCPServer):
    """MCP Server for Similarweb."""

    name: str = "similarweb"
    category: str = "Similarweb"
    description: str = "Similarweb integration for website analytics and market intelligence."
    scope: str = "similarweb_access_key"
    client_service = IntegrationAppClient()
    base_url = "/similarweb"

    def _register_prompts(self) -> None:
        """Register all Similarweb prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Similarweb tools with the MCP server."""

        get_company_by_domain_output = mcp_output(
            description="Website analytics including traffic, engagement metrics, traffic sources, and audience data",
            examples=[''])
        @self._mcp.tool(
            description="Get company and website analytics information by domain.",
            meta=mcp_meta("get_company_by_domain"),
            structured_output=True
        )
        async def get_company_by_domain(
            domain: Annotated[str, Field(description="Company domain (e.g., 'example.com')")]
        ) -> get_company_by_domain_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/company/domain/",
                data={"domain": domain},
                context=context
            )
            return [json.dumps(response.data)]
