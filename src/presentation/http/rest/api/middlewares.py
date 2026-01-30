import structlog
import uuid
from starlette.middleware.base import BaseHTTPMiddleware


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        corr_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))

        structlog.contextvars.bind_contextvars(correlation_id=corr_id)

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = corr_id
        return response
