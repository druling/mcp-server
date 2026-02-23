from src.servers.druling.workflow_component.mcp import WorkflowComponentServer
from src.servers.google.gmail.mcp import GmailServer

# Initialize MCP servers
workflow_server = WorkflowComponentServer()
gmail_server = GmailServer()

INTERNAL_MCP_PATH = {
    "workflow_component": workflow_server,
}

INTEGRATION_MCP_PATH = {
    "gmail": gmail_server,
}

MCP_PATH = {
    **INTERNAL_MCP_PATH,
    **INTEGRATION_MCP_PATH,
}

def mount_mcp_servers(app):
    """Mount MCP servers to the FastAPI app."""
    for key, server in MCP_PATH.items():
        app.mount(f"/{key}", server.streamable_http_app())
