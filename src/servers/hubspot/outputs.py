from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class Property(BaseModel):
    """HubSpot property"""
    name: str = Field(description="Property name")
    label: str = Field(description="Property label")
    type: str = Field(description="Property type")
    description: Optional[str] = Field(default=None, description="Property description")


class PropertyList(BaseModel):
    """List of properties"""
    properties: List[Dict[str, Any]] = Field(description="List of properties")


class Pipeline(BaseModel):
    """HubSpot pipeline"""
    id: str = Field(description="Pipeline ID")
    label: str = Field(description="Pipeline label")
    stages: Optional[List[Dict[str, Any]]] = Field(default=None, description="Pipeline stages")


class PipelineList(BaseModel):
    """List of pipelines"""
    pipelines: List[Dict[str, Any]] = Field(description="List of pipelines")


class ListInfo(BaseModel):
    """HubSpot list information"""
    listId: str = Field(description="List ID")
    name: str = Field(description="List name")
    objectTypeId: str = Field(description="Object type ID")


class Lists(BaseModel):
    """List of HubSpot lists"""
    lists: List[Dict[str, Any]] = Field(description="List of lists")


class Record(BaseModel):
    """HubSpot record"""
    id: Optional[str] = Field(default=None, description="Record ID")
    properties: Dict[str, Any] = Field(description="Record properties")


class RecordList(BaseModel):
    """List of records"""
    records: List[Dict[str, Any]] = Field(description="List of records")
    count: int = Field(description="Total number of records")


class RecordResult(BaseModel):
    """Result of record operation"""
    success: bool = Field(description="Whether the operation was successful")
    id: Optional[str] = Field(default=None, description="Record ID")
    message: Optional[str] = Field(default=None, description="Status message")


class EmailResult(BaseModel):
    """Result of email operation"""
    success: bool = Field(description="Whether the email was sent successfully")
    message: Optional[str] = Field(default=None, description="Status message")

