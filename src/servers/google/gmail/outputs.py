from typing import Optional
from pydantic import BaseModel, Field

# Pydantic models for structured output
class GmailRead(BaseModel):
    id: str = Field(description="Unique identifier for the workflow component")
    name: str = Field(description="Name of the workflow component")
    category: str = Field(description="Category of the workflow component")
    operation: str = Field(description="Operation type of the workflow component")
    description: Optional[str] = Field(default=None, description="Description of the workflow component")
    base_cost: Optional[str] = Field(default=None, description="Base cost of the workflow component")

class ListGmailRead(BaseModel):
    result: list[GmailRead] = Field(description="List of workflow components")
