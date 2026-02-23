from typing import Optional, List
from pydantic import BaseModel, Field


class Contact(BaseModel):
    """Hunter contact data"""
    first_name: Optional[str] = Field(default=None, description="First name")
    last_name: Optional[str] = Field(default=None, description="Last name")
    email: Optional[str] = Field(default=None, description="Email address")
    job_title: Optional[str] = Field(default=None, description="Job title")
    company: Optional[str] = Field(default=None, description="Company name")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn profile URL")
    phone: Optional[str] = Field(default=None, description="Phone number")
    confidence: Optional[int] = Field(default=None, description="Confidence score")


class ContactList(BaseModel):
    """List of contacts"""
    contacts: List[Contact] = Field(description="List of contacts")
    count: int = Field(description="Total number of contacts")

