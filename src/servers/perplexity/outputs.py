from typing import Optional
from pydantic import BaseModel, Field


class ReserveResult(BaseModel):
    """Perplexity credit reservation result"""
    success: bool = Field(description="Whether credit was reserved successfully")
    message: str = Field(description="Status message")

