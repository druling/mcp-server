import logging

from src.clients.backend.client import BackendClient
from src.clients.backend.dtos.request.credit import CreditData
from src.clients.backend.dtos.response.base import BaseResponse

logger = logging.getLogger(__name__)


class Credit(BackendClient):
    def __init__(self):
        super().__init__()
        self.base = "/credit"

    def reserve(self, usage_id, profile_id, amount) -> BaseResponse:
        request = CreditData(usage_id=usage_id, profile_id=profile_id, amount=amount)
        response = self._make_request(
            f"{self.base}/reserve/", method="POST", data=request.model_dump()
        )
        return self._process_response(response, BaseResponse)

    def revert(self, usage_id, profile_id, amount) -> BaseResponse:
        request = CreditData(usage_id=usage_id, profile_id=profile_id, amount=amount)
        response = self._make_request(
            f"{self.base}/revert/", method="POST", data=request.model_dump()
        )
        return self._process_response(response, BaseResponse)

    def confirm(self, usage_id, profile_id, amount) -> BaseResponse:
        request = CreditData(usage_id=usage_id, profile_id=profile_id, amount=amount)
        response = self._make_request(
            f"{self.base}/confirm/", method="POST", data=request.model_dump()
        )
        return self._process_response(response, BaseResponse)