from typing import Any, Dict
from pydantic import BaseModel, Field


class DocumentRead(BaseModel):
    """Structure for document read response"""
    content: str = Field(description="The text content of the document")
    title: str = Field(description="The title of the document")
    document_id: str = Field(description="The ID of the document")


class DocumentCreate(BaseModel):
    """Structure for document creation response"""
    document_id: str = Field(description="The ID of the created document")
    document_url: str = Field(description="The URL to view the document")
    title: str = Field(description="The title of the document")


class DocumentUpdate(BaseModel):
    """Structure for document update response"""
    document_id: str = Field(description="The ID of the updated document")
    success: bool = Field(description="Whether the update was successful")


class TabList(BaseModel):
    """Structure for document tabs"""
    tabs: list[Dict[str, Any]] = Field(description="List of tabs in the document")


class PlaceholderList(BaseModel):
    """Structure for document placeholders"""
    placeholders: list[str] = Field(description="List of placeholders found in the document")

