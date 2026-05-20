import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Apify prompts with the MCP server."""

    @mcp.prompt()
    async def apify_guide() -> str:
        return """Guide for using Apify API for web scraping and automation:

        Apify provides a cloud platform for running web scrapers and automation tasks:
        - Run pre-built actors or custom scrapers
        - Retrieve results from datasets
        - Access key-value stores for run artifacts

        Key capabilities:
        1. Actors: List available actors, run actors with custom input
        2. Runs: Monitor runs, get run status and results
        3. Datasets: Retrieve scraped data from datasets
        4. Key-Value Stores: Access run outputs and artifacts

        Best practices:
        - Use run_actor with appropriate memory and timeout settings
        - Poll get_run to monitor run status before fetching results
        - Use dataset offset/limit for paginating large datasets
        """
