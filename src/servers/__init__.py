from src.servers.druling import INTERNAL_MCP_SERVERS
from src.servers.google import GOOGLE_MCP_SERVERS
from src.servers.atlassian import ATLASSIAN_MCP_SERVERS

# Integration Services
from src.servers.apollo.mcp import ApolloServer
from src.servers.exa.mcp import ExaServer
from src.servers.firecrawl.mcp import FirecrawlServer
from src.servers.github.mcp import GithubServer
from src.servers.gong.mcp import GongServer
from src.servers.hubspot.mcp import HubspotServer
from src.servers.hunter.mcp import HunterServer
from src.servers.notion.mcp import NotionServer
from src.servers.slack.mcp import SlackServer
from src.servers.zerobounce.mcp import ZerobounceServer
from src.servers.similarweb.mcp import SimilarwebServer

# Initialize Integration MCP servers
apollo_server = ApolloServer()
exa_server = ExaServer()
firecrawl_server = FirecrawlServer()
github_server = GithubServer()
gong_server = GongServer()
hubspot_server = HubspotServer()
hunter_server = HunterServer()
notion_server = NotionServer()
slack_server = SlackServer()
zerobounce_server = ZerobounceServer()
similarweb_server = SimilarwebServer()

# Integration MCP servers mapping
INTEGRATION_MCP_SERVERS = {
    "apollo": apollo_server,
    "exa": exa_server,
    "firecrawl": firecrawl_server,
    "github": github_server,
    "gong": gong_server,
    "hubspot": hubspot_server,
    "hunter": hunter_server,
    "notion": notion_server,
    "slack": slack_server,
    "zerobounce": zerobounce_server,
    "similarweb": similarweb_server,
    **GOOGLE_MCP_SERVERS,
    **ATLASSIAN_MCP_SERVERS,
}

# Combined MCP servers mapping
MCP_SERVERS = {
    **INTERNAL_MCP_SERVERS,
    **INTEGRATION_MCP_SERVERS,
}

__all__ = [
    INTERNAL_MCP_SERVERS,
    INTEGRATION_MCP_SERVERS,
    MCP_SERVERS,
]
