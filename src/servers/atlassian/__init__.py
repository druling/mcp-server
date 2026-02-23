from src.servers.atlassian.confluence.mcp import ConfluenceServer
from src.servers.atlassian.jira.mcp import JiraServer

# Initialize Atlassian MCP servers
confluence_server = ConfluenceServer()
jira_server = JiraServer()

# Atlassian MCP servers mapping
ATLASSIAN_MCP_SERVERS = {
    "confluence": confluence_server,
    "jira": jira_server,
}

__all__ = [
    ATLASSIAN_MCP_SERVERS,
]

