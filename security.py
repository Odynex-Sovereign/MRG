"""Security headers, rate limiting helpers, and input sanitization."""

from __future__ import annotations

import time
from collections import defaultdict, deque
from threading import Lock

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        # CSP tuned for our static assets + inline critical styles; tighten further in production if needed
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: blob:; "
            "font-src 'self' data:; "
            "connect-src 'self' ws: wss:; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


class SimpleRateLimiter:
    """In-memory sliding-window rate limiter (per process). Suitable for single-instance Fly machines."""

    def __init__(self, requests_per_minute: int = 120) -> None:
        self.rpm = requests_per_minute
        self._hits: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        window = 60.0
        with self._lock:
            timestamps = self._hits[key]
            while timestamps and now - timestamps[0] >= window:
                timestamps.popleft()

            if len(timestamps) >= self.rpm:
                return False

            timestamps.append(now)
            if not timestamps:
                self._hits.pop(key, None)
            return True


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter: SimpleRateLimiter) -> None:
        super().__init__(app)
        self.limiter = limiter

    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip health checks
        if request.url.path in ("/healthz", "/readyz", "/livez"):
            return await call_next(request)
        client = request.client.host if request.client else "unknown"
        if not self.limiter.allow(client):
            return JSONResponse(
                {"detail": "Rate limit exceeded. Please try again shortly."},
                status_code=429,
                headers={"Retry-After": "60"},
            )
        return await call_next(request)
