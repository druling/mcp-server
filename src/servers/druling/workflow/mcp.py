import logging
from typing import Optional
from dataclasses import dataclass

from mcp.types import (
    Tool,
    Prompt,
    PromptArgument,
)

from src.core.service import BaseMCPServer

logger = logging.getLogger(__name__)


@dataclass
class WorkflowMCPServer(BaseMCPServer):
    """MCP Server for Druling Workflow operations."""

    name: str = "druling-workflow"

    def _register_tools(self) -> None:
        """Register all workflow tools with the MCP server."""

        @self._mcp.tool()
        async def create_workflow(
            name: str,
            description: str = "",
            steps: list[dict] = None,
        ) -> dict:
            """Create a new workflow."""
            user_ctx = self.get_user_context()
            workflow_id = f"wf_{user_ctx.user_id}_{name.lower().replace(' ', '_')}"
            return {
                "workflow_id": workflow_id,
                "name": name,
                "description": description,
                "steps": steps or [],
                "created_by": user_ctx.user_id,
                "entity_id": user_ctx.entity_id,
                "status": "created",
            }

        @self._mcp.tool()
        async def execute_workflow(
            workflow_id: str,
            input_data: dict = None,
        ) -> dict:
            """Execute a workflow by ID."""
            user_ctx = self.get_user_context()
            return {
                "execution_id": f"exec_{workflow_id}",
                "workflow_id": workflow_id,
                "input_data": input_data or {},
                "status": "running",
                "executed_by": user_ctx.user_id,
            }

        @self._mcp.tool()
        async def get_workflow_status(
            workflow_id: str,
            execution_id: Optional[str] = None,
        ) -> dict:
            """Get the status of a workflow or specific execution."""
            user_ctx = self.get_user_context()
            return {
                "workflow_id": workflow_id,
                "execution_id": execution_id,
                "status": "completed",
                "progress": 100,
                "user_id": user_ctx.user_id,
            }

        @self._mcp.tool()
        async def list_workflows(
            limit: int = 10,
            offset: int = 0,
            status: Optional[str] = None,
        ) -> dict:
            """List all workflows for the current user."""
            user_ctx = self.get_user_context()
            return {
                "workflows": [],
                "total": 0,
                "limit": limit,
                "offset": offset,
                "user_id": user_ctx.user_id,
                "entity_id": user_ctx.entity_id,
            }

        @self._mcp.tool()
        async def delete_workflow(workflow_id: str) -> dict:
            """Delete a workflow by ID."""
            user_ctx = self.get_user_context()
            return {
                "workflow_id": workflow_id,
                "status": "deleted",
                "deleted_by": user_ctx.user_id,
            }

    def _register_prompts(self) -> None:
        """Register all workflow prompts with the MCP server."""

        @self._mcp.prompt()
        async def workflow_creation_guide(workflow_type: str = "general") -> str:
            """Get a comprehensive guide for creating workflows."""
            try:
                user_ctx = self.get_user_context()
                logger.info(f"Getting workflow creation guide for user: {user_ctx.user_id}")
            except ValueError:
                logger.info("Getting workflow creation guide (no user context)")

            return f"Guide for creating {workflow_type} workflows..."

        @self._mcp.prompt()
        async def workflow_troubleshooting(error_type: str = "", workflow_id: str = "") -> str:
            """Get troubleshooting guidance for workflow errors."""
            return f"Troubleshooting guide for error: {error_type}, workflow: {workflow_id}"

        @self._mcp.prompt()
        async def workflow_optimization() -> str:
            """Get optimization suggestions for improving workflow performance and reliability."""
            return "Optimization suggestions for workflows..."

    def get_tool_definitions(self) -> list[Tool]:
        """Get all tool definitions for this server."""
        return [
            Tool(
                name="create_workflow",
                description="Create a new workflow with specified name, description, and steps",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "The name of the workflow"},
                        "description": {"type": "string", "description": "Optional description of the workflow"},
                        "steps": {"type": "array", "items": {"type": "object"}, "description": "List of workflow steps"}
                    },
                    "required": ["name"]
                }
            ),
            Tool(
                name="execute_workflow",
                description="Execute a workflow by its ID with optional input data",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "workflow_id": {"type": "string", "description": "The ID of the workflow to execute"},
                        "input_data": {"type": "object", "description": "Input data for the workflow execution"}
                    },
                    "required": ["workflow_id"]
                }
            ),
            Tool(
                name="get_workflow_status",
                description="Get the status of a workflow or specific execution",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "workflow_id": {"type": "string", "description": "The ID of the workflow"},
                        "execution_id": {"type": "string", "description": "Optional specific execution ID"}
                    },
                    "required": ["workflow_id"]
                }
            ),
            Tool(
                name="list_workflows",
                description="List all workflows for the current user with pagination",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Maximum number of workflows to return", "default": 10},
                        "offset": {"type": "integer", "description": "Offset for pagination", "default": 0},
                        "status": {"type": "string", "description": "Filter by workflow status"}
                    }
                }
            ),
            Tool(
                name="delete_workflow",
                description="Delete a workflow by its ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "workflow_id": {"type": "string", "description": "The ID of the workflow to delete"}
                    },
                    "required": ["workflow_id"]
                }
            )
        ]

    def get_prompt_definitions(self) -> list[Prompt]:
        """Get all prompt definitions for this server."""
        return [
            Prompt(
                name="workflow_creation_guide",
                description="Get a comprehensive guide for creating workflows",
                arguments=[
                    PromptArgument(
                        name="workflow_type",
                        description="The type of workflow to create (e.g., general, data-processing, automation)",
                        required=False
                    )
                ]
            ),
            Prompt(
                name="workflow_troubleshooting",
                description="Get troubleshooting guidance for workflow errors",
                arguments=[
                    PromptArgument(name="error_type", description="The type of error encountered", required=False),
                    PromptArgument(name="workflow_id", description="Optional workflow ID for context", required=False)
                ]
            ),
            Prompt(
                name="workflow_optimization",
                description="Get optimization suggestions for improving workflow performance and reliability",
                arguments=[]
            )
        ]
