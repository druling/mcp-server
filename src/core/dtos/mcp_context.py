from typing import Optional
from pydantic import BaseModel, Field

class MCPContext(BaseModel):
    """Initialization parameters for the MCP server."""
    user_id: str = Field(..., description="The user ID for authentication")
    secret_id: str = Field(..., description="The secret ID for authentication")
    entity_id: Optional[str] = Field(None, description="Optional workspace ID")
    entity_type: Optional[str] = Field(None, description="Optional workspace type")

    class Config:
        extra = "forbid"