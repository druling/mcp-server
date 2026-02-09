import logging

from src.clients.base import BaseClient
from src.setup.config import config

logger = logging.getLogger(__name__)


class BackendClient(BaseClient):
    def __init__(self):
        super().__init__(config.backend_url, config.timeout)
