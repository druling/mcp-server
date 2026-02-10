import logging
from typing import Dict

from src.clients.backend.dtos.response.base import BaseResponse
from src.clients.base import BaseClient
from src.setup.config import config

logger = logging.getLogger(__name__)


class BackendClient(BaseClient):
    def __init__(self):
        super().__init__(config.backend_url, config.timeout)

    def get(self, endpoint: str, params: dict = None) -> BaseResponse | Dict:
        response = self.make_request(endpoint=endpoint, method="GET", params=params)
        return self._process_response(response, BaseResponse)

    def post(self, endpoint: str, data: dict = None) -> BaseResponse | Dict:
        response = self.make_request(endpoint=endpoint, method="POST", data=data)
        return self._process_response(response, BaseResponse)

