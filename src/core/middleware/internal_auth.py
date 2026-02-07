import logging
from typing import Optional

logger = logging.getLogger(__name__)


class InternalAuth:
    """Internal token authentication handler."""

    def __init__(self, expected_token: Optional[str] = None):
        self.expected_token = expected_token

    def verify_token(self, token: str) -> bool:
        """Verify the internal token."""
        if self.expected_token is None:
            logger.warning("No expected token configured, skipping verification")
            return True
        return token == self.expected_token

    def authenticate(self, token: str) -> dict:
        """Authenticate using internal token and return user context."""
        if not self.verify_token(token):
            raise ValueError("Invalid internal token")
        return {"authenticated": True, "token_verified": True}
