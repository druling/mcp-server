from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field


class DriveFile(BaseModel):
    """Structure for a Google Drive file"""
    id: str = Field(description="The unique ID of the file")
    name: str = Field(description="The name of the file")
    mimeType: Optional[str] = Field(default=None, description="The MIME type of the file")
    webViewLink: Optional[str] = Field(default=None, description="URL to view the file in a browser")
    createdTime: Optional[str] = Field(default=None, description="When the file was created")
    modifiedTime: Optional[str] = Field(default=None, description="When the file was last modified")


class SearchResult(BaseModel):
    """Structure for search results"""
    files: List[DriveFile] = Field(description="List of files found")
    count: int = Field(description="Number of files found")


class FileOperation(BaseModel):
    """Structure for file operations"""
    file_id: str = Field(description="The ID of the file")
    file_url: Optional[str] = Field(default=None, description="The URL of the file")


class FolderCreate(BaseModel):
    """Structure for folder creation response"""
    folder_id: str = Field(description="The ID of the created folder")
    folder_url: str = Field(description="The URL to view the folder")


class FileUpload(BaseModel):
    """Structure for file upload response"""
    file_url: str = Field(description="The URL of the uploaded file")


class FileRead(BaseModel):
    """Structure for file read response"""
    file_path: str = Field(description="Path to the downloaded file")
    file_id: str = Field(description="The ID of the file")
    name: str = Field(description="The name of the file")
    mime_type: str = Field(description="The MIME type of the file")
    web_view_link: str = Field(description="URL to view the file in a browser")


class FolderContents(BaseModel):
    """Structure for folder contents"""
    files: List[Dict[str, Any]] = Field(description="List of files in the folder")
    count: int = Field(description="Number of files in the folder")


class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool = Field(description="Whether the operation was successful")
    message: Optional[str] = Field(default=None, description="Status message")

