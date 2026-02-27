import logging
from typing import Dict

from src.clients.backend.dtos.response.base import BaseResponse
from src.clients.base import BaseClient
from src.core.dtos.mcp_context import MCPContext
from src.core.utils import get_mcp_context_header
from src.setup.config import config

logger = logging.getLogger(__name__)


class BackendClient(BaseClient):
    def __init__(self):
        backend_url = f"{config.backend_url}/internal/integration"
        super().__init__(backend_url, config.timeout)

    def get(self, endpoint: str, params: dict = None, context: MCPContext = None) -> BaseResponse | Dict:
        headers = get_mcp_context_header(context)
        response = self.make_request(endpoint=endpoint, method="GET", params=params, headers=headers)
        return self._process_response(response, BaseResponse)

    def post(self, endpoint: str, data: dict = None, context = None) -> BaseResponse | Dict:
        headers = get_mcp_context_header(context)
        response = self.make_request(endpoint=endpoint, method="POST", data=data, headers=headers)
        return self._process_response(response, BaseResponse)
