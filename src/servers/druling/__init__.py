from src.servers.druling.workflow.mcp import WorkflowServer
from src.servers.druling.workflow_component.mcp import WorkflowComponentServer
from src.servers.druling.workflow_run.mcp import WorkflowRunServer
from src.servers.druling.task_scheduler.mcp import TaskSchedulerServer

# Initialize Druling Internal MCP servers
workflow_server = WorkflowServer()
workflow_component_server = WorkflowComponentServer()
workflow_run_server = WorkflowRunServer()
task_scheduler_server = TaskSchedulerServer()

# Internal MCP servers mapping
INTERNAL_MCP_SERVERS = {
    "workflow": workflow_server,
    "workflow_component": workflow_component_server,
    "workflow_run": workflow_run_server,
    "task_scheduler": task_scheduler_server,
}

__all__ = [
    INTERNAL_MCP_SERVERS,
]
