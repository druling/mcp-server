import logging


from src.clients.backend.client import BackendClient
from src.clients.backend.dtos.response.secret import SecretResponse

logger = logging.getLogger(__name__)


class Secret(BackendClient):
    def __init__(self):
        super().__init__()
        self.base = "/secret"

    def fetch(self, profile_id, secret_type) -> SecretResponse:
        """
        Send a query to the AI server and return the response.
        """
        response = self._make_request(
            f"{self.base}/type/{profile_id}/{secret_type}", method="GET"
        )
        return self._process_response(response, SecretResponse)
