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
class WorkflowRunServer(BaseMCPServer):
    """MCP Server for Workflow Run."""

    name: str = "workflow_run"
    category: str = "Workflow Run"
    description: str = "Manage and monitor workflow execution runs and their status."
    scope: str = "workflow_run_access"

    backend_service = BackendClient()
    base_url = "/workflow_run"

    def _register_prompts(self) -> None:
        """Register all Workflow Run prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Workflow Run tools with the MCP server."""

        get_all_components_output = mcp_output(
            description="List of all workflow runs with IDs, status, start time, and execution details",
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
            description="Workflow run details including ID, status, execution logs, and output data",
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
            description="List of workflow runs matching the query with status and execution details",
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
