from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import Any, Optional, Dict


class BaseResponse(BaseModel):
    status: int
    data: Dict[str, Any]

    def __init__(self, data: Any = None, message: Optional[str] = None, status_code: Optional[int] = None, **kwargs):
        # Convert data to JSON-serializable format if needed
        serialized_data = self._serialize_data(data)

        super().__init__(
            status=status_code,
            data={
                "success": status_code is None or status_code < 400,
                "message": message,
                "data": serialized_data,
                **kwargs
            }
        )

    def _serialize_data(self, data: Any) -> Any:
        """Convert data to JSON-serializable format"""
        if data is None:
            return None

        # Handle Pydantic models
        if hasattr(data, 'dict') and callable(getattr(data, 'dict')):
            return data.dict()

        # Handle dictionaries with Pydantic models as values
        if isinstance(data, dict):
            return {
                key: self._serialize_data(value)
                for key, value in data.items()
            }

        # Handle iterables (lists, tuples, sets, generators, etc.) but not strings
        if hasattr(data, '__iter__') and not isinstance(data, (str, bytes, dict)):
            return [self._serialize_data(item) for item in data]

        # For everything else (primitives), return as-is
        # FastAPI's JSONResponse will handle the serialization
        return data

    def to_json_response(self) -> JSONResponse:
        """Convert the response to FastAPI JSONResponse"""
        return JSONResponse(
            content=self.data,
            status_code=self.status
        )


class SuccessResponse(BaseResponse):
    def __init__(self, data: Any = None, message: str = "Operation successful", **kwargs):
        super().__init__(
            data=data,
            message=message,
            status_code=200,
            **kwargs
        )


class CreatedResponse(BaseResponse):
    def __init__(self, data: Any = None, message: str = "Resource created successfully", **kwargs):
        super().__init__(
            data=data,
            message=message,
            status_code=201,
            **kwargs
        )


class BadRequestResponse(BaseResponse):
    def __init__(
        self,
        data=None,
        message="Bad requests",
        status=500,
        error_code=None,
        errors=None,
        **kwargs,
    ):
        super().__init__(
            data=data,
            message=message,
            errors=errors,
            status=status,
            error_code=error_code,
            **kwargs,
        )


class ResponseFactory:
    @staticmethod
    def success(data: Any = None, message: str = "Operation successful", **kwargs) -> JSONResponse:
        response = SuccessResponse(data=data, message=message, **kwargs)
        return response.to_json_response()

    @staticmethod
    def created(data: Any = None, message: str = "Resource created successfully", **kwargs) -> JSONResponse:
        response = CreatedResponse(data=data, message=message, **kwargs)
        return response.to_json_response()

    @staticmethod
    def response(
            status_code: int, data: Any = None, message: str = "Custom response", **kwargs
            ) -> JSONResponse:
        """Create a custom response with a specific status code"""
        response = BaseResponse(data=data, message=message, status_code=status_code, **kwargs)
        return response.to_json_response()

    @staticmethod
    def error(
        data=None,
        message="Something went wrong",
        status=500,
        error_code=None,
        errors=None,
        **kwargs,
    ):
        return BadRequestResponse(
            data=data,
            message=message,
            status=status,
            error_code=error_code,
            errors=errors,
            **kwargs,
        )
