import logging
from typing import Annotated, Optional, Dict, List, Any
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from . import outputs
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class GoogleSheetServer(BaseMCPServer):
    """MCP Server for Google Sheets."""

    name: str = "google_sheets"
    category: str = "Google Sheets"
    description: str = "Google Sheets integration for managing spreadsheets and data."
    scope: str = "google_sheets_access"
    backend_service = BackendClient()
    base_url = "/google/gsheet"

    def _register_prompts(self) -> None:
        """Register all Google Sheets prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Google Sheets tools with the MCP server."""

        @self._mcp.tool(
            description="Create new rows in a Google Sheet.",
            meta=mcp_meta("create_rows"),
            structured_output=True
        )
        async def create_rows(
            sheet_name: Annotated[str, Field(description="Name of the sheet to add rows to")],
            values: Annotated[Dict[str, Any], Field(description="Dictionary of column headers and values to add")],
            spreadsheet_id: Annotated[Optional[str], Field(description="The ID of the spreadsheet")] = None,
            spreadsheet_url: Annotated[Optional[str], Field(description="The URL of the spreadsheet")] = None
        ) -> outputs.SheetCreate:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/create/",
                data={
                    "spreadsheet_id": spreadsheet_id,
                    "spreadsheet_url": spreadsheet_url,
                    "sheet_name": sheet_name,
                    "values": values
                },
                context=context
            )
            return outputs.SheetCreate(**response.data)

        @self._mcp.tool(
            description="Read data from a Google Sheet with optional filtering.",
            meta=mcp_meta("read_sheet"),
            structured_output=True
        )
        async def read_sheet(
            sheet_name: Annotated[str, Field(description="Name of the sheet to read")],
            spreadsheet_id: Annotated[Optional[str], Field(description="The ID of the spreadsheet")] = None,
            spreadsheet_url: Annotated[Optional[str], Field(description="The URL of the spreadsheet")] = None,
            row_range: Annotated[Optional[str], Field(description="Range of rows to read (e.g., 'A1:Z100')")] = None,
            search_column: Annotated[Optional[str], Field(description="Column name to search in")] = None,
            search_values: Annotated[Optional[List[str]], Field(description="Values to search for")] = None,
            num_rows: Annotated[Optional[int], Field(description="Number of rows to return")] = None,
            preserve_formatting: Annotated[Optional[bool], Field(description="Whether to preserve cell formatting")] = False,
            reverse: Annotated[Optional[bool], Field(description="Whether to reverse the order of rows")] = False
        ) -> outputs.SheetData:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/list/",
                data={
                    "spreadsheet_id": spreadsheet_id,
                    "spreadsheet_url": spreadsheet_url,
                    "sheet_name": sheet_name,
                    "row_range": row_range,
                    "search_column": search_column,
                    "search_values": search_values,
                    "num_rows": num_rows,
                    "preserve_formatting": preserve_formatting,
                    "reverse": reverse
                },
                context=context
            )
            return outputs.SheetData(**response.data)

        @self._mcp.tool(
            description="Get list of all sheets in a spreadsheet.",
            meta=mcp_meta("get_sheets"),
            structured_output=True
        )
        async def get_sheets(
            spreadsheet_id: Annotated[Optional[str], Field(description="The ID of the spreadsheet")] = None,
            spreadsheet_url: Annotated[Optional[str], Field(description="The URL of the spreadsheet")] = None
        ) -> outputs.SheetList:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/sheets/",
                data={
                    "spreadsheet_id": spreadsheet_id,
                    "spreadsheet_url": spreadsheet_url
                },
                context=context
            )
            return outputs.SheetList(**response.data)

        @self._mcp.tool(
            description="Get column names from a sheet.",
            meta=mcp_meta("get_columns"),
            structured_output=True
        )
        async def get_columns(
            sheet_name: Annotated[str, Field(description="Name of the sheet")],
            spreadsheet_id: Annotated[Optional[str], Field(description="The ID of the spreadsheet")] = None,
            spreadsheet_url: Annotated[Optional[str], Field(description="The URL of the spreadsheet")] = None
        ) -> outputs.ColumnList:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/batch/get/",
                data={
                    "spreadsheet_id": spreadsheet_id,
                    "spreadsheet_url": spreadsheet_url,
                    "sheet_name": sheet_name
                },
                context=context
            )
            return outputs.ColumnList(**response.data)

        @self._mcp.tool(
            description="Update rows in a sheet based on filter criteria.",
            meta=mcp_meta("update_rows"),
            structured_output=True
        )
        async def update_rows(
            sheet_name: Annotated[str, Field(description="Name of the sheet")],
            filter_column: Annotated[str, Field(description="Column name to filter by")],
            filter_value: Annotated[str, Field(description="Value to filter for")],
            update_values: Annotated[Dict[str, Any], Field(description="Dictionary of column names and new values")],
            spreadsheet_id: Annotated[Optional[str], Field(description="The ID of the spreadsheet")] = None,
            spreadsheet_url: Annotated[Optional[str], Field(description="The URL of the spreadsheet")] = None,
            upsert: Annotated[Optional[bool], Field(description="Whether to insert a new row if no match is found")] = False
        ) -> outputs.SheetCreate:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/batch/update/",
                data={
                    "spreadsheet_id": spreadsheet_id,
                    "spreadsheet_url": spreadsheet_url,
                    "sheet_name": sheet_name,
                    "filter_column": filter_column,
                    "filter_value": filter_value,
                    "update_values": update_values,
                    "upsert": upsert
                },
                context=context
            )
            return outputs.SheetCreate(**response.data)

        @self._mcp.tool(
            description="Append values to a specific column in a sheet.",
            meta=mcp_meta("append_values"),
            structured_output=True
        )
        async def append_values(
            sheet_name: Annotated[str, Field(description="Name of the sheet")],
            column_header: Annotated[str, Field(description="Header of the column to append to")],
            values: Annotated[List[Any], Field(description="List of values to append")],
            spreadsheet_id: Annotated[Optional[str], Field(description="The ID of the spreadsheet")] = None,
            spreadsheet_url: Annotated[Optional[str], Field(description="The URL of the spreadsheet")] = None
        ) -> outputs.SheetCreate:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/values/append/",
                data={
                    "spreadsheet_id": spreadsheet_id,
                    "spreadsheet_url": spreadsheet_url,
                    "sheet_name": sheet_name,
                    "column_header": column_header,
                    "values": values
                },
                context=context
            )
            return outputs.SheetCreate(**response.data)

        @self._mcp.tool(
            description="Find rows in a sheet by searching in a specific column.",
            meta=mcp_meta("find_rows"),
            structured_output=True
        )
        async def find_rows(
            sheet_name: Annotated[str, Field(description="Name of the sheet")],
            search_column: Annotated[str, Field(description="Column name to search in")],
            search_values: Annotated[List[str], Field(description="Values to search for")],
            spreadsheet_id: Annotated[Optional[str], Field(description="The ID of the spreadsheet")] = None,
            spreadsheet_url: Annotated[Optional[str], Field(description="The URL of the spreadsheet")] = None
        ) -> outputs.SheetData:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/find-row/",
                data={
                    "spreadsheet_id": spreadsheet_id,
                    "spreadsheet_url": spreadsheet_url,
                    "sheet_name": sheet_name,
                    "search_column": search_column,
                    "search_values": search_values
                },
                context=context
            )
            return outputs.SheetData(**response.data)

        @self._mcp.tool(
            description="Clear values from a range in a sheet.",
            meta=mcp_meta("clear_values"),
            structured_output=True
        )
        async def clear_values(
            sheet_name: Annotated[str, Field(description="Name of the sheet")],
            spreadsheet_id: Annotated[Optional[str], Field(description="The ID of the spreadsheet")] = None,
            spreadsheet_url: Annotated[Optional[str], Field(description="The URL of the spreadsheet")] = None,
            range: Annotated[Optional[str], Field(description="Range to clear (e.g., 'A1:B10'). If not provided, clears entire sheet")] = None
        ) -> outputs.SuccessResponse:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/values/clear/",
                data={
                    "spreadsheet_id": spreadsheet_id,
                    "spreadsheet_url": spreadsheet_url,
                    "sheet_name": sheet_name,
                    "range": range
                },
                context=context
            )
            return outputs.SuccessResponse(success=True, message="Values cleared successfully")

        @self._mcp.tool(
            description="Copy a sheet to create a duplicate.",
            meta=mcp_meta("copy_sheet"),
            structured_output=True
        )
        async def copy_sheet(
            sheet_name: Annotated[str, Field(description="Name of the sheet to copy")],
            new_sheet_name: Annotated[str, Field(description="Name for the new copied sheet")],
            spreadsheet_id: Annotated[Optional[str], Field(description="The ID of the spreadsheet")] = None,
            spreadsheet_url: Annotated[Optional[str], Field(description="The URL of the spreadsheet")] = None
        ) -> outputs.SheetCreate:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/copy/",
                data={
                    "spreadsheet_id": spreadsheet_id,
                    "spreadsheet_url": spreadsheet_url,
                    "sheet_name": sheet_name,
                    "new_sheet_name": new_sheet_name
                },
                context=context
            )
            return outputs.SheetCreate(**response.data)

        @self._mcp.tool(
            description="Add a new sheet to a spreadsheet.",
            meta=mcp_meta("add_sheet"),
            structured_output=True
        )
        async def add_sheet(
            sheet_name: Annotated[str, Field(description="Name of the new sheet to add")],
            spreadsheet_id: Annotated[Optional[str], Field(description="The ID of the spreadsheet")] = None,
            spreadsheet_url: Annotated[Optional[str], Field(description="The URL of the spreadsheet")] = None
        ) -> outputs.SheetCreate:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/add-sheet/",
                data={
                    "spreadsheet_id": spreadsheet_id,
                    "spreadsheet_url": spreadsheet_url,
                    "sheet_name": sheet_name
                },
                context=context
            )
            return outputs.SheetCreate(**response.data)
