from src.servers.druling.workflow_component.mcp import WorkflowComponentMCPServer
from src.servers.google.gmail.mcp import GmailMCPServer

# Initialize MCP servers
workflow_server = WorkflowComponentMCPServer()
gmail_server = GmailMCPServer()

MCP_PATH = {
    "workflow_component": workflow_server,
    "gmail": gmail_server,
}

async def register_mcp_servers(stack):
    for server in MCP_PATH.values():
        await stack.enter_async_context(server.mcp.session_manager.run())


def mount_mcp_servers(app):
    """Mount MCP servers to the FastAPI app."""
    for key, server in MCP_PATH.items():
        app.mount(f"/{key}", server.streamable_http_app())
