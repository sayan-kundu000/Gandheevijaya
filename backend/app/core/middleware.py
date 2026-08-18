import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from backend.app.core.logging import request_id_ctx_var

logger = logging.getLogger("gandheevijaya.access")


class RequestCorrelationMiddleware(BaseHTTPMiddleware):
    """
    Middleware that manages the X-Request-ID correlation header across requests,
    injects it into the asynchronous ContextVar for logging, and attaches it to the HTTP response.
    Also logs request timing and method/status code.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Extract or generate Request Correlation ID
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = f"req_{uuid.uuid4().hex[:16]}"

        # Set ContextVar token
        token = request_id_ctx_var.set(request_id)
        start_time = time.perf_counter()

        try:
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.4f}s"

            # Log standard access metrics
            logger.info(
                f"{request.method} {request.url.path} -> {response.status_code} ({process_time * 1000:.2f}ms)"
            )
            return response
        except Exception as exc:
            process_time = time.perf_counter() - start_time
            logger.error(
                f"{request.method} {request.url.path} -> ERROR ({process_time * 1000:.2f}ms): {exc}"
            )
            raise
        finally:
            request_id_ctx_var.reset(token)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):

    """
    Middleware that attaches modern HTTP security headers to all API responses
    to defend against clickjacking, MIME-sniffing, and cross-site scripting vulnerabilities.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        return response

