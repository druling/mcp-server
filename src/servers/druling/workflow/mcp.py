import logging
from typing import Optional, Annotated
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from src.servers.druling.workflow import outputs
from src.servers.druling.workflow.prompts import workflow_prompts

logger = logging.getLogger(__name__)


@dataclass
class WorkflowMCPServer(BaseMCPServer):
    """MCP Server for Druling Workflow operations."""

    name: str = "druling-workflow"
    backend_service = BackendClient()
    base_url = "/workflow_component"

    def _register_prompts(self) -> None:
        """Register all workflow prompts with the MCP server."""
        workflow_prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all workflow tools with the MCP server."""

        @self._mcp.tool(
            description="Get all workflow components/nodes that are present in the system.",
            meta=mcp_meta("get_all_components"),
            structured_output=True,
        )
        async def get_all_components() -> list[outputs.WorkflowComponent]:
            response = self.backend_service.get(f"{self.base_url}/all/")
            result = []
            for component in response.data:
                result.append(outputs.WorkflowComponent(
                    id=component.get("id"),
                    name=component.get("name"),
                    operation=component.get("operation"),
                    description=component.get("description"),
                    category=component.get("category"),
                    base_cost=component.get("base_cost"),
                ))
            return result

        @self._mcp.tool(
            description="Get a workflow by its ID.",
            meta=mcp_meta("get_by_id"),
            structured_output=True,
        )
        async def get_by_id(
            workflow_id: Annotated[str, Field(description="The ID of the workflow to execute")]
        ) -> outputs.WorkflowComponent:
            response = self.backend_service.get(f"{self.base_url}/{workflow_id}/")
            return outputs.WorkflowComponent(
                    id=response.get("id"),
                    name=response.get("name"),
                    operation=response.get("operation"),
                    description=response.get("description"),
                    category=response.get("category"),
                    base_cost=response.get("base_cost"),
                )

        @self._mcp.tool(
            description="Get the status of a workflow or specific execution.",
            meta=mcp_meta("get_workflow_status"),
            structured_output=True,
        )
        async def get_workflow_status(
            workflow_id: Annotated[str, Field(description="The ID of the workflow to check")],
            execution_id: Annotated[Optional[str], Field(description="Optional specific execution ID to check status for")] = None,
        ) -> outputs.WorkflowStatusOutput:
            user_ctx = self.get_context()
            return outputs.WorkflowStatusOutput(
                workflow_id=workflow_id,
                execution_id=execution_id,
                status="completed",
                progress=100,
                user_id=user_ctx.user_id,
            )

        @self._mcp.tool(
            description="List all workflows for the current user with pagination.",
            meta=mcp_meta("list_workflows"),
            structured_output=True,
        )
        async def list_workflows(
            limit: Annotated[int, Field(description="Maximum number of workflows to return")] = 10,
            offset: Annotated[int, Field(description="Offset for pagination")] = 0,
            status: Annotated[Optional[str], Field(description="Filter by workflow status")] = None,
        ) -> outputs.ListWorkflowsOutput:
            user_ctx = self.get_context()
            return outputs.ListWorkflowsOutput(
                workflows=[],
                total=0,
                limit=limit,
                offset=offset,
                user_id=user_ctx.user_id,
                entity_id=user_ctx.entity_id,
            )

        @self._mcp.tool(
            description="Delete a workflow by its ID.",
            meta=mcp_meta("delete_workflow"),
            structured_output=True,
        )
        async def delete_workflow(
            workflow_id: Annotated[str, Field(description="The ID of the workflow to delete")],
        ) -> outputs.DeleteWorkflowOutput:
            user_ctx = self.get_context()
            return outputs.DeleteWorkflowOutput(
                workflow_id=workflow_id,
                status="deleted",
                deleted_by=user_ctx.user_id,
            )
