import logging
from typing import Annotated
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from src.servers.druling.workflow_component import outputs
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

        @self._mcp.tool(
            description="Get all workflow components/nodes that are present in the system.",
            meta=mcp_meta("get_all_components"),
            structured_output=True,
        )
        async def get_all_components() -> outputs.ListWorkflowComponent:
            response = self.backend_service.get(f"{self.base_url}/all/")
            result: list[outputs.WorkflowComponent] = response.data
            return outputs.ListWorkflowComponent(result=result)

        @self._mcp.tool(
            description="Get a workflow by its ID.",
            meta=mcp_meta("get_by_id"),
            structured_output=True,
        )
        async def get_by_id(
            workflow_id: Annotated[str, Field(description="The ID of the workflow to execute")]
        ) -> outputs.WorkflowComponent:
            response = self.backend_service.get(f"{self.base_url}/{workflow_id}/")
            response = response.data
            return outputs.WorkflowComponent(
                    id=response.get("id"),
                    name=response.get("name"),
                    operation=response.get("operation"),
                    description=response.get("description"),
                    category=response.get("category"),
                    base_cost=response.get("base_cost"),
                )

        @self._mcp.tool(
            description="Search component by name, category or operation.",
            meta=mcp_meta("search_component"),
            structured_output=True,
        )
        async def search_component(
            query: Annotated[str, Field(description="Search component by name, category or operation.")],
        ) -> outputs.ListWorkflowComponent:
            response = self.backend_service.get(f"{self.base_url}/search/", params={
                "query": query
            })
            result = [
                outputs.WorkflowComponent(
                    id=item.get("id"),
                    name=item.get("name"),
                    operation=item.get("operation"),
                    description=item.get("description"),
                    category=item.get("category"),
                    base_cost=item.get("base_cost"),
                )
                for item in response.data
            ]
            return outputs.ListWorkflowComponent(result=result)
