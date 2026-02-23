from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class Company(BaseModel):
    """Apollo company data"""
    id: Optional[str] = Field(default=None, description="Company ID")
    name: Optional[str] = Field(default=None, description="Company name")
    domain: Optional[str] = Field(default=None, description="Company domain")
    industry: Optional[str] = Field(default=None, description="Company industry")
    size: Optional[str] = Field(default=None, description="Company size range")
    location: Optional[str] = Field(default=None, description="Company location")
    description: Optional[str] = Field(default=None, description="Company description")


class CompanyList(BaseModel):
    """List of companies"""
    companies: List[Company] = Field(description="List of companies")
    count: int = Field(description="Total number of companies")


class Contact(BaseModel):
    """Apollo contact data"""
    id: Optional[str] = Field(default=None, description="Contact ID")
    first_name: Optional[str] = Field(default=None, description="First name")
    last_name: Optional[str] = Field(default=None, description="Last name")
    email: Optional[str] = Field(default=None, description="Email address")
    job_title: Optional[str] = Field(default=None, description="Job title")
    company: Optional[str] = Field(default=None, description="Company name")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn profile URL")
    phone: Optional[str] = Field(default=None, description="Phone number")


class ContactList(BaseModel):
    """List of contacts"""
    contacts: List[Contact] = Field(description="List of contacts")
    count: int = Field(description="Total number of contacts")

