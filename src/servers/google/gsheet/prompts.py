import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Google Sheets prompts with the MCP server."""

    @mcp.prompt()
    async def google_sheets_guide() -> str:
        return """
# Google Sheets MCP Tools Guide

This guide provides information about available Google Sheets tools for managing spreadsheets.

## Available Tools:

### 1. create_rows
Create new rows in a sheet.
- Parameters: spreadsheet_id or spreadsheet_url, sheet_name, values (dict)
- Returns: Updated spreadsheet information

### 2. read_sheet
Read data from a sheet with filtering options.
- Parameters: spreadsheet_id or spreadsheet_url, sheet_name, row_range, search_column, search_values, num_rows, preserve_formatting, reverse
- Returns: Sheet data as list of dictionaries

### 3. get_sheets
Get list of all sheets in a spreadsheet.
- Parameters: spreadsheet_id or spreadsheet_url
- Returns: List of sheet names

### 4. get_columns
Get column names/headers from a sheet.
- Parameters: spreadsheet_id or spreadsheet_url, sheet_name
- Returns: List of column names

### 5. update_rows
Update rows based on filter criteria (with optional upsert).
- Parameters: spreadsheet_id or spreadsheet_url, sheet_name, filter_column, filter_value, update_values, upsert
- Returns: Update status

### 6. append_values
Append values to a specific column.
- Parameters: spreadsheet_id or spreadsheet_url, sheet_name, column_header, values (list)
- Returns: Update status

### 7. find_rows
Find rows by searching in a specific column.
- Parameters: spreadsheet_id or spreadsheet_url, sheet_name, search_column, search_values
- Returns: Matching rows

### 8. clear_values
Clear values from a range or entire sheet.
- Parameters: spreadsheet_id or spreadsheet_url, sheet_name, range (optional)
- Returns: Success status

### 9. copy_sheet
Create a duplicate of a sheet.
- Parameters: spreadsheet_id or spreadsheet_url, sheet_name, new_sheet_name
- Returns: New sheet information

### 10. add_sheet
Add a new sheet to a spreadsheet.
- Parameters: spreadsheet_id or spreadsheet_url, sheet_name
- Returns: New sheet information

## Usage Tips:
- Values parameter in create_rows should be: {"Column1": "value1", "Column2": "value2"}
- Use upsert=true in update_rows to insert if no match is found
- row_range format: 'A1:Z100'
- search_values is a list of values to search for
"""
