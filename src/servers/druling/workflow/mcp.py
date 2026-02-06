import logging
from typing import Any, Optional
from dataclasses import dataclass, field

from mcp.server.fastmcp import FastMCP
from mcp.types import (
    Tool,
    TextContent,
    Prompt,
    PromptMessage,
    PromptArgument,
    GetPromptResult,
)

from src.core.dtos.mcp_context import MCPContext
from src.core.middleware import InternalAuth

logger = logging.getLogger(__name__)


@dataclass
class WorkflowMCPServer:
    """
    MCP Server for Druling Workflow operations.

    This server provides:
    - Tools for workflow management
    - Prompts for workflow interactions
    - Internal token authentication
    - Initialization with user_id and secret_id
    """

    name: str = "druling-workflow"
    version: str = "1.0.0"
    user_id: Optional[str] = None
    secret_id: Optional[str] = None
    workspace_id: Optional[str] = None
    internal_token: Optional[str] = None
    _mcp: FastMCP = field(init=False)
    _auth: InternalAuth = field(init=False)
    _initialized: bool = field(default=False, init=False)

    def __post_init__(self):
        """Initialize the MCP server and register handlers."""
        self._mcp = FastMCP(
            name=self.name,
            version=self.version,
        )
        self._auth = InternalAuth(expected_token=self.internal_token)
        self._register_tools()
        self._register_prompts()
        logger.info(f"WorkflowMCPServer initialized: {self.name} v{self.version}")

    def initialize(self, params: MCPContext) -> dict:
        """
        Initialize the server with user credentials.

        Args:
            params: Initialization parameters containing user_id and secret_id

        Returns:
            dict: Initialization result with status
        """
        self.user_id = params.user_id
        self.secret_id = params.secret_id
        self.workspace_id = params.workspace_id
        self._initialized = True

        logger.info(f"Server initialized for user: {self.user_id}")

        return {
            "status": "initialized",
            "user_id": self.user_id,
            "workspace_id": self.workspace_id,
        }

    def authenticate_internal(self, token: str) -> dict:
        """
        Authenticate using internal token.

        Args:
            token: The internal authentication token

        Returns:
            dict: Authentication result

        Raises:
            ValueError: If authentication fails
        """
        return self._auth.authenticate(token)

    def _check_initialized(self) -> None:
        """Check if the server is properly initialized."""
        if not self._initialized:
            raise RuntimeError("Server not initialized. Call initialize() first.")

    # ==================== TOOLS ====================

    def _register_tools(self) -> None:
        """Register all workflow tools with the MCP server."""

        @self._mcp.tool()
        async def create_workflow(
            name: str,
            description: str = "",
            steps: list[dict] = None,
        ) -> dict:
            """
            Create a new workflow.

            Args:
                name: The name of the workflow
                description: Optional description of the workflow
                steps: List of workflow steps

            Returns:
                dict: The created workflow details
            """
            self._check_initialized()

            workflow_id = f"wf_{self.user_id}_{name.lower().replace(' ', '_')}"

            return {
                "workflow_id": workflow_id,
                "name": name,
                "description": description,
                "steps": steps or [],
                "created_by": self.user_id,
                "workspace_id": self.workspace_id,
                "status": "created",
            }

        @self._mcp.tool()
        async def execute_workflow(
            workflow_id: str,
            input_data: dict = None,
        ) -> dict:
            """
            Execute a workflow by ID.

            Args:
                workflow_id: The ID of the workflow to execute
                input_data: Input data for the workflow execution

            Returns:
                dict: Execution result
            """
            self._check_initialized()

            return {
                "execution_id": f"exec_{workflow_id}",
                "workflow_id": workflow_id,
                "input_data": input_data or {},
                "status": "running",
                "executed_by": self.user_id,
            }

        @self._mcp.tool()
        async def get_workflow_status(
            workflow_id: str,
            execution_id: Optional[str] = None,
        ) -> dict:
            """
            Get the status of a workflow or specific execution.

            Args:
                workflow_id: The ID of the workflow
                execution_id: Optional specific execution ID

            Returns:
                dict: Workflow/execution status
            """
            self._check_initialized()

            return {
                "workflow_id": workflow_id,
                "execution_id": execution_id,
                "status": "completed",
                "progress": 100,
            }

        @self._mcp.tool()
        async def list_workflows(
            limit: int = 10,
            offset: int = 0,
            status: Optional[str] = None,
        ) -> dict:
            """
            List all workflows for the current user.

            Args:
                limit: Maximum number of workflows to return
                offset: Offset for pagination
                status: Filter by workflow status

            Returns:
                dict: List of workflows
            """
            self._check_initialized()

            return {
                "workflows": [],
                "total": 0,
                "limit": limit,
                "offset": offset,
                "user_id": self.user_id,
                "workspace_id": self.workspace_id,
            }

        @self._mcp.tool()
        async def delete_workflow(
            workflow_id: str,
        ) -> dict:
            """
            Delete a workflow by ID.

            Args:
                workflow_id: The ID of the workflow to delete

            Returns:
                dict: Deletion result
            """
            self._check_initialized()

            return {
                "workflow_id": workflow_id,
                "status": "deleted",
                "deleted_by": self.user_id,
            }

    # ==================== PROMPTS ====================

    def _register_prompts(self) -> None:
        """Register all workflow prompts with the MCP server."""

        @self._mcp.prompt()
        async def workflow_creation_guide(
            workflow_type: str = "general",
        ) -> GetPromptResult:
            """
            Get a guide for creating workflows.

            Args:
                workflow_type: The type of workflow to create
            """
            return GetPromptResult(
                description=f"Guide for creating a {workflow_type} workflow",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(
                            type="text",
                            text=f"""I want to create a {workflow_type} workflow. 
Please help me define the following:
1. Workflow name and description
2. Input parameters required
3. Steps to execute
4. Output format
5. Error handling strategy"""
                        )
                    )
                ]
            )

        @self._mcp.prompt()
        async def workflow_troubleshooting(
            error_type: str = "general",
            workflow_id: Optional[str] = None,
        ) -> GetPromptResult:
            """
            Get troubleshooting guidance for workflow errors.

            Args:
                error_type: The type of error encountered
                workflow_id: Optional workflow ID for context
            """
            context = f"Workflow ID: {workflow_id}" if workflow_id else "No specific workflow"

            return GetPromptResult(
                description=f"Troubleshooting guide for {error_type} errors",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(
                            type="text",
                            text=f"""I'm experiencing a {error_type} error in my workflow.
{context}

Please help me:
1. Identify the root cause
2. Suggest fixes
3. Prevent this issue in the future"""
                        )
                    )
                ]
            )

        @self._mcp.prompt()
        async def workflow_optimization() -> GetPromptResult:
            """Get optimization suggestions for workflows."""
            return GetPromptResult(
                description="Workflow optimization suggestions",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(
                            type="text",
                            text="""Please analyze my workflow and suggest optimizations for:
1. Performance improvements
2. Resource efficiency
3. Error resilience
4. Maintainability"""
                        )
                    )
                ]
            )

    # ==================== TOOL DEFINITIONS ====================

    def get_tool_definitions(self) -> list[Tool]:
        """
        Get all tool definitions for this server.

        Returns:
            list[Tool]: List of tool definitions
        """
        return [
            Tool(
                name="create_workflow",
                description="Create a new workflow with specified name, description, and steps",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the workflow"
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional description of the workflow"
                        },
                        "steps": {
                            "type": "array",
                            "items": {"type": "object"},
                            "description": "List of workflow steps"
                        }
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
                        "workflow_id": {
                            "type": "string",
                            "description": "The ID of the workflow to execute"
                        },
                        "input_data": {
                            "type": "object",
                            "description": "Input data for the workflow execution"
                        }
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
                        "workflow_id": {
                            "type": "string",
                            "description": "The ID of the workflow"
                        },
                        "execution_id": {
                            "type": "string",
                            "description": "Optional specific execution ID"
                        }
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
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of workflows to return",
                            "default": 10
                        },
                        "offset": {
                            "type": "integer",
                            "description": "Offset for pagination",
                            "default": 0
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by workflow status"
                        }
                    }
                }
            ),
            Tool(
                name="delete_workflow",
                description="Delete a workflow by its ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "workflow_id": {
                            "type": "string",
                            "description": "The ID of the workflow to delete"
                        }
                    },
                    "required": ["workflow_id"]
                }
            )
        ]

    # ==================== PROMPT DEFINITIONS ====================

    def get_prompt_definitions(self) -> list[Prompt]:
        """
        Get all prompt definitions for this server.

        Returns:
            list[Prompt]: List of prompt definitions
        """
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
                    PromptArgument(
                        name="error_type",
                        description="The type of error encountered",
                        required=False
                    ),
                    PromptArgument(
                        name="workflow_id",
                        description="Optional workflow ID for context",
                        required=False
                    )
                ]
            ),
            Prompt(
                name="workflow_optimization",
                description="Get optimization suggestions for improving workflow performance and reliability",
                arguments=[]
            )
        ]
