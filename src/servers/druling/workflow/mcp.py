import logging
from typing import Optional, Annotated
from dataclasses import dataclass

from pydantic import Field

from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from src.servers.druling.workflow.outputs import CreateWorkflowOutput, ExecuteWorkflowOutput, WorkflowStatusOutput, \
    ListWorkflowsOutput, DeleteWorkflowOutput
from src.servers.druling.workflow.prompts import workflow_prompts

logger = logging.getLogger(__name__)


@dataclass
class WorkflowMCPServer(BaseMCPServer):
    """MCP Server for Druling Workflow operations."""

    name: str = "druling-workflow"

    def _register_prompts(self) -> None:
        """Register all workflow prompts with the MCP server."""
        workflow_prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all workflow tools with the MCP server."""

        @self._mcp.tool(
            description="Create a new workflow with specified name, description, and steps.",
            meta=mcp_meta("create_workflow"),
            structured_output=True,
        )
        async def create_workflow(
            name: Annotated[str, Field(description="The name of the workflow")],
            description: Annotated[str, Field(description="Optional description of the workflow")] = "",
            steps: Annotated[list[dict], Field(description="List of workflow steps as dictionaries")] = None,
        ) -> CreateWorkflowOutput:
            user_ctx = self.get_context()
            workflow_id = f"wf_{user_ctx.user_id}_{name.lower().replace(' ', '_')}"
            return CreateWorkflowOutput(
                workflow_id=workflow_id,
                name=name,
                description=description,
                steps=steps or [],
                created_by=user_ctx.user_id,
                entity_id=user_ctx.entity_id,
                status="created",
            )

        @self._mcp.tool(
            description="Execute a workflow by its ID with optional input data.",
            meta=mcp_meta("execute_workflow"),
            structured_output=True,
        )
        async def execute_workflow(
            workflow_id: Annotated[str, Field(description="The ID of the workflow to execute")],
            input_data: Annotated[dict, Field(description="Input data for the workflow execution")] = None,
        ) -> ExecuteWorkflowOutput:
            user_ctx = self.get_context()
            return ExecuteWorkflowOutput(
                execution_id=f"exec_{workflow_id}",
                workflow_id=workflow_id,
                input_data=input_data or {},
                status="running",
                executed_by=user_ctx.user_id,
            )

        @self._mcp.tool(
            description="Get the status of a workflow or specific execution.",
            meta=mcp_meta("get_workflow_status"),
            structured_output=True,
        )
        async def get_workflow_status(
            workflow_id: Annotated[str, Field(description="The ID of the workflow to check")],
            execution_id: Annotated[Optional[str], Field(description="Optional specific execution ID to check status for")] = None,
        ) -> WorkflowStatusOutput:
            user_ctx = self.get_context()
            return WorkflowStatusOutput(
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
        ) -> ListWorkflowsOutput:
            user_ctx = self.get_context()
            return ListWorkflowsOutput(
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
        ) -> DeleteWorkflowOutput:
            user_ctx = self.get_context()
            return DeleteWorkflowOutput(
                workflow_id=workflow_id,
                status="deleted",
                deleted_by=user_ctx.user_id,
            )
