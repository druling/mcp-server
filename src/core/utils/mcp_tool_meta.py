def mcp_meta(id: str, credit_cost: int = None, scopes: list[str] = None):
    """Decorator to add metadata to MCP tools."""
    if scopes is None:
        scopes = []

    return {
        "id": id,
        "creditCost": credit_cost,
        "scopes": scopes,
    }