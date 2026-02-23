from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class CompanyInfo(BaseModel):
    """Similarweb company information"""
    domain: str = Field(description="Company domain")
    name: Optional[str] = Field(default=None, description="Company name")
    description: Optional[str] = Field(default=None, description="Company description")
    global_rank: Optional[int] = Field(default=None, description="Global website rank")
    country_rank: Optional[int] = Field(default=None, description="Country website rank")
    category: Optional[str] = Field(default=None, description="Website category")
    monthly_visits: Optional[int] = Field(default=None, description="Monthly visits")
    traffic_sources: Optional[Dict[str, Any]] = Field(default=None, description="Traffic sources breakdown")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

