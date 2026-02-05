from mcp.server.auth import BearerAuth

def mcp_auth():
    return BearerAuth(
        issuer="workflow-engine",
        audience="mcp-platform",
        jwks_url="http://localhost:8000/.well-known/jwks.json"
    )