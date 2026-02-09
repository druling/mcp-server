from typing import Optional, List, Dict

from pydantic import BaseModel

from src.clients.backend.dtos.response.base import BaseResponse

class SecretBaseResponse(BaseModel):
    """Base response model"""

    id: str
    resource: Optional[str] = None
    secret_type: Optional[str] = None
    scopes: Optional[List[str]] = None
    is_default: Optional[bool] = False
    key: Optional[Dict] = None

SecretResponse = BaseResponse[SecretBaseResponse]
