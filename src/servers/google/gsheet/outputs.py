from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field


class SheetData(BaseModel):
    """Structure for sheet data response"""
    data: List[Dict[str, Any]] = Field(description="List of rows as dictionaries")
    spreadsheet_id: str = Field(description="ID of the spreadsheet")
    sheet_name: str = Field(description="Name of the sheet")


class SheetList(BaseModel):
    """Structure for sheet list response"""
    sheets: List[str] = Field(description="List of sheet names")


class ColumnList(BaseModel):
    """Structure for column list response"""
    columns: List[str] = Field(description="List of column names")


class SheetCreate(BaseModel):
    """Structure for sheet creation/update response"""
    spreadsheet_id: str = Field(description="ID of the spreadsheet")
    sheet_id: Optional[str] = Field(default=None, description="ID of the sheet")
    sheet_name: Optional[str] = Field(default=None, description="Name of the sheet")
    sheet_url: Optional[str] = Field(default=None, description="URL to view the sheet")
    updated_rows: Optional[int] = Field(default=None, description="Number of rows updated")


class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool = Field(description="Whether the operation was successful")
    message: Optional[str] = Field(default=None, description="Status message")

