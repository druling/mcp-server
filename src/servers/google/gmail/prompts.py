import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Gmail prompts with the MCP server."""

    @mcp.prompt()
    async def gmail_guide() -> str:
        return """
# Gmail MCP Tools Guide

This guide provides information about available Gmail tools for managing emails.

## Available Tools:

### 1. read_emails
Read emails from Gmail account with optional search filters.
- Parameters: query, max_results
- Returns: List of emails with subject, sender, body, etc.

### 2. send_email
Send an email or create a draft. Can also reply to threads.
- Parameters: to, subject, body, html_body, attachments, thread_id, save_as_draft, is_reply
- Returns: Message ID and thread ID

### 3. update_email
Update email properties (mark as read, add/remove labels).
- Parameters: message_id, mark_as_read, add_labels, remove_labels
- Returns: Success status

### 4. create_draft
Create a draft email without sending.
- Parameters: to, subject, body, html_body, attachments
- Returns: Draft ID

### 5. forward_email
Forward an email to another recipient.
- Parameters: to, subject, body, thread_id, save_as_draft
- Returns: Message ID and thread ID

### 6. create_label
Create a new label in Gmail.
- Parameters: label_name, label_list_visibility, message_list_visibility
- Returns: Label information

### 7. archive_email
Archive an email (remove from inbox).
- Parameters: message_id
- Returns: Success status

### 8. trash_email
Move an email to trash.
- Parameters: message_id
- Returns: Success status

### 9. star_email
Star an email for importance.
- Parameters: message_id
- Returns: Success status

### 10. unstar_email
Remove star from an email.
- Parameters: message_id
- Returns: Success status

### 11. get_attachment
Download an attachment from an email.
- Parameters: message_id, attachment_id
- Returns: Attachment file URL and metadata

### 12. list_labels
Get all labels in the Gmail account.
- Returns: List of labels

## Usage Tips:
- Search queries support Gmail operators: from:, to:, subject:, has:attachment, is:unread
- Use thread_id with is_reply=true to reply to existing emails
- Label visibility options: 'labelShow', 'labelShowIfUnread', 'labelHide'
"""
