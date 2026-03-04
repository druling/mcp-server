import uuid
import time
import logging

from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

logger = logging.getLogger(__name__)


class RequestIDMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = str(uuid.uuid4())
        request = Request(scope, receive)
        request.state.request_id = request_id

        old_factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            record.request_id = request_id
            return record

        logging.setLogRecordFactory(record_factory)

        status_code: list[int] = [0]
        start_time = time.time()

        async def send_wrapper(message: dict):
            if message["type"] == "http.response.start":
                status_code[0] = message.get("status", 0)
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
            process_time = time.time() - start_time
            logger.info(
                f"{request.method} {request.url.path}",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": status_code[0],
                    "execution_time": round(process_time, 4),
                    "user_agent": request.headers.get("user-agent", ""),
                    "client_ip": request.client.host if request.client else "",
                },
            )
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Request failed: {request.method} {request.url.path}",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "execution_time": round(process_time, 4),
                    "error": str(e),
                },
                exc_info=True,
            )
            raise
        finally:
            logging.setLogRecordFactory(old_factory)
