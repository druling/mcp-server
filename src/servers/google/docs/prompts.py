import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Google Docs prompts with the MCP server."""

    @mcp.prompt()
    async def google_docs_guide() -> str:
        return """
# Google Docs MCP Tools Guide

This guide provides information about available Google Docs tools for managing documents.

## Available Tools:

### 1. read_document
Read content from a Google Doc document.
- Parameters: document_id or document_url, optional tabs list
- Returns: Document content, title, and ID

### 2. create_document
Create a new Google Doc document.
- Parameters: title, content, format_type (plain_text/html), folder_id, mark_as_public
- Returns: Document ID and URL

### 3. update_document
Update an existing Google Doc with new content.
- Parameters: document_id or document_url, content, format_type, upsert_start
- Returns: Update status and document ID

### 4. list_document_tabs
List all tabs in a Google Doc document.
- Parameters: document_id or document_url
- Returns: List of tabs

### 5. create_from_template
Create a new document from a template with placeholder replacements.
- Parameters: document_name, template_id or template_url, placeholders, folder_id, make_public
- Returns: New document ID and URL

### 6. find_placeholders
Find all placeholders in a template document.
- Parameters: template_id or template_url
- Returns: List of placeholders found

## Usage Tips:
- You can use either document_id or document_url for most operations
- Placeholders typically use {{placeholder_name}} format
- format_type can be 'plain_text' or 'html'
"""
