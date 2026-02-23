import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Google Slides prompts with the MCP server."""

    @mcp.prompt()
    async def google_slides_guide() -> str:
        return """
# Google Slides MCP Tools Guide

This guide provides information about available Google Slides tools for managing presentations.

## Available Tools:

### 1. read_slides
Read content from slides in a presentation.
- Parameters: presentation_id or presentation_url, index_start, index_end, thumbnail_size
- Returns: Presentation information with slide contents and thumbnails

### 2. create_from_template
Create a new presentation from a template with placeholder replacements.
- Parameters: template_id or template_url, new_title, replacements (dict)
- Returns: New presentation ID and URL

### 3. find_placeholders
Find all placeholders in a template presentation.
- Parameters: template_id or template_url
- Returns: List of placeholders found

## Usage Tips:
- thumbnail_size options: 'SMALL', 'MEDIUM', 'LARGE'
- Placeholders typically use {{placeholder_name}} format
- Replacements should be a dictionary: {"{{title}}": "My Title", "{{author}}": "John Doe"}
- Use index_start and index_end to read specific slide ranges
"""
