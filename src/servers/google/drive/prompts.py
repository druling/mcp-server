import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Google Drive prompts with the MCP server."""

    @mcp.prompt()
    async def google_drive_guide() -> str:
        return """
# Google Drive MCP Tools Guide

This guide provides information about available Google Drive tools for managing files and folders.

## Available Tools:

### 1. search_files
Search for files in Google Drive using queries.
- Parameters: query, max_results
- Returns: List of matching files with metadata

### 2. copy_file
Create a copy of a file.
- Parameters: file_id or file_url, new_title
- Returns: New file ID and URL

### 3. create_folder
Create a new folder in Google Drive.
- Parameters: folder_name, parent_folder_id (optional)
- Returns: Folder ID and URL

### 4. move_file
Move a file to a different folder.
- Parameters: file_id or file_url, destination_folder_id
- Returns: Updated file information

### 5. upload_file
Upload a plain text file to Google Drive.
- Parameters: file_name, file_content, parent_folder_id (optional)
- Returns: File URL

### 6. change_permissions
Change sharing permissions for a file.
- Parameters: file_id or file_url, permission_type, permission_role, email_address, domain, send_notification
- Returns: Success status

### 7. rename_file
Rename a file in Google Drive.
- Parameters: file_id or file_url, new_name
- Returns: Updated file information

### 8. get_file
Download/retrieve a file from Google Drive.
- Parameters: file_id or file_url
- Returns: File path and metadata

### 9. list_folder_contents
List all contents of a folder.
- Parameters: folder_id or folder_url, recursive, only_drive_link, only_doc_link
- Returns: List of files in folder

### 10. delete_file
Delete a file or folder from Google Drive.
- Parameters: file_id or file_url
- Returns: Success status

## Usage Tips:
- Search queries support operators like: name contains "text", mimeType="application/pdf"
- Permission types: 'anyone', 'user', 'group', 'domain'
- Permission roles: 'reader', 'writer', 'commenter'
"""
