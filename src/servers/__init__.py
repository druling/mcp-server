from src.servers.druling import INTERNAL_MCP_SERVERS
from src.servers.google import GOOGLE_MCP_SERVERS
from src.servers.atlassian import ATLASSIAN_MCP_SERVERS

# Integration Services
from src.servers.affinity.mcp import AffinityServer
from src.servers.apollo.mcp import ApolloServer
from src.servers.apify.mcp import ApifyServer
from src.servers.ashby.mcp import AshbyServer
from src.servers.asana.mcp import AsanaServer
from src.servers.browserbase.mcp import BrowserbaseServer
from src.servers.cal.mcp import CalServer
from src.servers.exa.mcp import ExaServer
from src.servers.firecrawl.mcp import FirecrawlServer
from src.servers.ghost.mcp import GhostServer
from src.servers.github.mcp import GithubServer
from src.servers.gong.mcp import GongServer
from src.servers.hubspot.mcp import HubspotServer
from src.servers.hunter.mcp import HunterServer
from src.servers.incident_io.mcp import IncidentIoServer
from src.servers.linear.mcp import LinearServer
from src.servers.luma.mcp import LumaServer
from src.servers.notion.mcp import NotionServer
from src.servers.parallel.mcp import ParallelServer
from src.servers.posthog.mcp import PosthogServer
from src.servers.slack.mcp import SlackServer
from src.servers.zerobounce.mcp import ZerobounceServer
from src.servers.similarweb.mcp import SimilarwebServer

# Initialize Integration MCP servers
affinity_server = AffinityServer()
apollo_server = ApolloServer()
apify_server = ApifyServer()
ashby_server = AshbyServer()
asana_server = AsanaServer()
browserbase_server = BrowserbaseServer()
cal_server = CalServer()
exa_server = ExaServer()
firecrawl_server = FirecrawlServer()
ghost_server = GhostServer()
github_server = GithubServer()
gong_server = GongServer()
hubspot_server = HubspotServer()
hunter_server = HunterServer()
incident_io_server = IncidentIoServer()
linear_server = LinearServer()
luma_server = LumaServer()
notion_server = NotionServer()
parallel_server = ParallelServer()
posthog_server = PosthogServer()
slack_server = SlackServer()
zerobounce_server = ZerobounceServer()
similarweb_server = SimilarwebServer()

# Integration MCP servers mapping
INTEGRATION_MCP_SERVERS = {
    "affinity": affinity_server,
    "apollo": apollo_server,
    "apify": apify_server,
    "ashby": ashby_server,
    "asana": asana_server,
    "browserbase": browserbase_server,
    "cal": cal_server,
    "exa": exa_server,
    "firecrawl": firecrawl_server,
    "ghost": ghost_server,
    "github": github_server,
    "gong": gong_server,
    "hubspot": hubspot_server,
    "hunter": hunter_server,
    "incident_io": incident_io_server,
    "linear": linear_server,
    "luma": luma_server,
    "notion": notion_server,
    "parallel": parallel_server,
    "posthog": posthog_server,
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
