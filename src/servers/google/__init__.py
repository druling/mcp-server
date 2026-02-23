from src.servers.google.gmail.mcp import GmailServer
from src.servers.google.docs.mcp import GoogleDocsServer
from src.servers.google.drive.mcp import GoogleDriveServer
from src.servers.google.meet.mcp import GoogleMeetServer
from src.servers.google.gsheet.mcp import GoogleSheetServer
from src.servers.google.slides.mcp import GoogleSlideServer

# Initialize Google MCP servers
gmail_server = GmailServer()
google_docs_server = GoogleDocsServer()
google_drive_server = GoogleDriveServer()
google_meet_server = GoogleMeetServer()
google_sheets_server = GoogleSheetServer()
google_slides_server = GoogleSlideServer()

# Google MCP servers mapping
GOOGLE_MCP_SERVERS = {
    "gmail": gmail_server,
    "google_docs": google_docs_server,
    "google_drive": google_drive_server,
    "google_meet": google_meet_server,
    "google_sheets": google_sheets_server,
    "google_slides": google_slides_server,
}

__all__ = [
    GOOGLE_MCP_SERVERS,
]

