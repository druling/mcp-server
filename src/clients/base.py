from __future__ import annotations

import logging

import requests
from typing import Optional, Dict, Any, Type

from src.clients.backend.dtos.response.base import BaseResponse
from src.core.enums.CustomHeader import CustomHeader
from src.core.exceptions import RateLimitExceeded, ErrorCode, BaseError
from src.setup.config import config

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self, url: str, timeout: int):
        self.base_url = url
        self.api_key = config.internal_secret
        self.timeout = timeout

    def make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
    ) -> Optional[Dict]:
        url = f"{self.base_url}{endpoint}"
        headers = {CustomHeader.X_INTERNAL_AUTH.value: f"{self.api_key}"}

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                timeout=self.timeout,
            )
            return response.json()
        except requests.RequestException as e:
            logger.error(
                f"Error communicating with {self.base_url} at endpoint {endpoint}: {str(e)}",
            )
            raise BaseError("Error communicating with internal service")

    def _process_response(
        self, response_data: Dict, response_class: Type
    ) -> BaseResponse | Dict:
        """Process response data into specified class"""
        try:
            response = self._parse_response(response_data, response_class)
            if response is None or response.success is False:

                if response.error_code in [ErrorCode.RATE_LIMIT_EXCEEDED.value]:
                    logger.error(f"Credit limit exceeded: {response_data}")
                    raise RateLimitExceeded(f"Credit limit exceeded")

                logger.error(f"Unsuccessful response: {response_data}")
                raise BaseError("Unsuccessful response from internal service")

            return response
        except Exception as e:
            logger.error(f"Error parsing response: {str(e)}")
            raise BaseError("Error parsing response from internal service")

    def _parse_response(self, response_data: Dict, response_class: Type) -> BaseResponse | Dict:
        """Parse JSON response safely"""
        if response_class == dict:
            return response_data
        elif hasattr(response_class, "__dataclass_fields__"):
            return response_class(**response_data) if response_data else None
        else:
            return response_class(**response_data) if response_data else None

    def _get_cached_response(self, cache_key: str) -> Optional[Any]:
        """Get cached response - implement caching logic"""
        # Implement your caching logic here
        return None

    def _cache_response(self, cache_key: str, response: Any, ttl: int):
        """Cache response - implement caching logic"""
        # Implement your caching logic here
        pass
