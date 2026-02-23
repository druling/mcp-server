from src.servers import MCP_SERVERS

def mount_mcp_servers(app):
    """Mount MCP servers to the FastAPI app."""
    for key, server in MCP_SERVERS.items():
        app.mount(f"/{key}", server.streamable_http_app())
