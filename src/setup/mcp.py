from src.servers.druling.workflow_component.mcp import WorkflowComponentMCPServer

# Initialize MCP servers
workflow_server = WorkflowComponentMCPServer()

async def register_mcp_servers(stack):
    await stack.enter_async_context(workflow_server.mcp.session_manager.run())

def mount_mcp_servers(app):
    """Mount MCP servers to the FastAPI app."""
    app.mount("/workflow_component", workflow_server.streamable_http_app())