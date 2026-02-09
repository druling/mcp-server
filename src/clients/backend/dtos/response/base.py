from typing import Optional, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    """Base response model"""

    success: bool
    data: Optional[T] = None
    message: Optional[str] = ""
    error: Optional[str] = None
    error_code: Optional[str] = None
