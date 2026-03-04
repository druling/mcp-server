import logging

from src.clients.backend.client.client import BackendClient

logger = logging.getLogger(__name__)


class IntegrationAppClient(BackendClient):
    def __init__(self):
        super().__init__("/integration")