from typing import Optional
from pydantic import BaseModel, Field

# Pydantic models for structured output
class CreateWorkflowOutput(BaseModel):
    """Output schema for create_workflow tool."""
    workflow_id: str = Field(description="Unique identifier for the created workflow")
    name: str = Field(description="Name of the workflow")
    description: str = Field(description="Description of the workflow")
    steps: list[dict] = Field(description="List of workflow steps")
    created_by: str = Field(description="User ID who created the workflow")
    entity_id: Optional[str] = Field(default=None, description="Entity ID associated with the workflow")
    status: str = Field(description="Current status of the workflow")


class ExecuteWorkflowOutput(BaseModel):
    """Output schema for execute_workflow tool."""
    execution_id: str = Field(description="Unique identifier for the execution")
    workflow_id: str = Field(description="ID of the executed workflow")
    input_data: dict = Field(description="Input data used for execution")
    status: str = Field(description="Execution status")
    executed_by: str = Field(description="User ID who executed the workflow")


class WorkflowStatusOutput(BaseModel):
    """Output schema for get_workflow_status tool."""
    workflow_id: str = Field(description="ID of the workflow")
    execution_id: Optional[str] = Field(default=None, description="Execution ID if provided")
    status: str = Field(description="Current status")
    progress: int = Field(description="Progress percentage")
    user_id: str = Field(description="User ID")


class ListWorkflowsOutput(BaseModel):
    """Output schema for list_workflows tool."""
    workflows: list[dict] = Field(description="List of workflows")
    total: int = Field(description="Total number of workflows")
    limit: int = Field(description="Limit used for pagination")
    offset: int = Field(description="Offset used for pagination")
    user_id: str = Field(description="User ID")
    entity_id: Optional[str] = Field(default=None, description="Entity ID")


class DeleteWorkflowOutput(BaseModel):
    """Output schema for delete_workflow tool."""
    workflow_id: str = Field(description="ID of the deleted workflow")
    status: str = Field(description="Deletion status")
    deleted_by: str = Field(description="User ID who deleted the workflow")
