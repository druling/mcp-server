import json
import logging
from typing import Annotated
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.outputs import mcp_output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class WorkflowComponentServer(BaseMCPServer):
    """MCP Server for Workflow component."""

    name: str = "workflow_component"
    category: str = "Workflow"
    description: str = "Manage and retrieve workflow components/nodes that can be used in building workflows."
    scope: str = ""

    backend_service = BackendClient()
    base_url = "/workflow_component"

    def _register_prompts(self) -> None:
        """Register all Workflow Component prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Workflow Component tools with the MCP server."""

        get_all_components_output = mcp_output(
            description="List of all available workflow components/nodes with names, categories, and supported operations",
            examples=[''])
        @self._mcp.tool(
            description="Get all workflow components/nodes that are present in the system.",
            meta=mcp_meta("get_all_components"),
            structured_output=True,
        )
        async def get_all_components() -> get_all_components_output:
            response = self.backend_service.get(f"{self.base_url}/all/")
            return [json.dumps(item) for item in response.data]

        get_by_id_output = mcp_output(
            description="Workflow component details including ID, name, input/output schema, and configuration",
            examples=[''])
        @self._mcp.tool(
            description="Get a workflow by its ID.",
            meta=mcp_meta("get_by_id"),
            structured_output=True,
        )
        async def get_by_id(
            workflow_id: Annotated[str, Field(description="The ID of the workflow to execute")]
        ) -> get_by_id_output:
            response = self.backend_service.get(f"{self.base_url}/{workflow_id}/")
            return [json.dumps(response.data)]

        search_component_output = mcp_output(
            description="List of workflow components matching the query with names, categories, and operations",
            examples=[''])
        @self._mcp.tool(
            description="Search component by name, category or operation.",
            meta=mcp_meta("search_component"),
            structured_output=True,
        )
        async def search_component(
            query: Annotated[str, Field(description="Search component by name, category or operation.")],
        ) -> search_component_output:
            response = self.backend_service.get(f"{self.base_url}/search/", params={
                "query": query
            })
            return [json.dumps(item) for item in response.data]
