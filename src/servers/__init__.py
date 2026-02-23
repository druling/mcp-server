from src.servers.druling import INTERNAL_MCP_SERVERS
from src.servers.google import GOOGLE_MCP_SERVERS
from src.servers.atlassian import ATLASSIAN_MCP_SERVERS

# Integration Services
from src.servers.apollo.mcp import ApolloServer
from src.servers.firecrawl.mcp import FirecrawlServer
from src.servers.hubspot.mcp import HubspotServer
from src.servers.hunter.mcp import HunterServer
from src.servers.perplexity.mcp import PerplexityServer
from src.servers.slack.mcp import SlackServer
from src.servers.zerobounce.mcp import ZerobounceServer
from src.servers.similarweb.mcp import SimilarwebServer

# Initialize Integration MCP servers
apollo_server = ApolloServer()
firecrawl_server = FirecrawlServer()
hubspot_server = HubspotServer()
hunter_server = HunterServer()
perplexity_server = PerplexityServer()
slack_server = SlackServer()
zerobounce_server = ZerobounceServer()
similarweb_server = SimilarwebServer()

# Integration MCP servers mapping
INTEGRATION_MCP_SERVERS = {
    "apollo": apollo_server,
    "firecrawl": firecrawl_server,
    "hubspot": hubspot_server,
    "hunter": hunter_server,
    "perplexity": perplexity_server,
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
