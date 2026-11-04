"""MRG FastAPI application factory."""

from __future__ import annotations

import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from mrg import __version__
from mrg.config import Settings, get_settings
from mrg.logging_config import setup_logging

logger = logging.getLogger("mrg")
_db_pool: Any = None
STATIC_ROOT = Path(__file__).resolve().parents[1] / "app"


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


class RequestTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Process-Time-Ms"] = f"{duration_ms:.2f}"
        if duration_ms > 1000:
            logger.warning(
                "slow_request",
                extra={
                    "path": request.url.path,
                    "method": request.method,
                    "duration_ms": duration_ms,
                },
            )
        return response


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings: Settings = app.state.settings
    setup_logging(settings)
    logger.info(
        "MRG starting",
        extra={
            "version": __version__,
            "environment": settings.environment,
            "sandbox": settings.sandbox_mode or not settings.has_deepseek,
        },
    )
    global _db_pool
    if settings.has_database:
        try:
            import asyncpg

            _db_pool = await asyncpg.create_pool(
                settings.database_url,
                min_size=settings.db_pool_min_size,
                max_size=settings.db_pool_max_size,
                command_timeout=settings.db_command_timeout,
            )
            app.state.db_pool = _db_pool
            logger.info("database_pool_ready")
        except Exception:
            logger.exception("database_pool_failed — continuing without DB")
            app.state.db_pool = None
    else:
        app.state.db_pool = None
        logger.info("no_database_configured — sandbox mode")
    yield
    if _db_pool is not None:
        await _db_pool.close()
        logger.info("database_pool_closed")
    logger.info("MRG shutdown complete")


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description=(
            "Planet-scale crisis simulation grid combining macro structural reasoning, "
            "low-latency micro-conversational avatars, and sensory engines."
        ),
        lifespan=lifespan,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
    )
    app.state.settings = settings

    app.add_middleware(RequestTimingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    if settings.trusted_hosts and settings.trusted_hosts != ["*"]:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.trusted_hosts)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    _register_routes(app, settings)
    return app


def _page(name: str) -> FileResponse:
    path = STATIC_ROOT / name
    if not path.is_file():
        path = STATIC_ROOT / "index.html"
    return FileResponse(path, media_type="text/html")


def _register_routes(app: FastAPI, settings: Settings) -> None:
    from mrg.api.health import router as health_router
    from mrg.api.pricing import router as pricing_router
    from mrg.api.websocket import router as ws_router

    app.include_router(health_router)
    app.include_router(ws_router)
    app.include_router(pricing_router)

    # Static assets (css/js)
    assets = STATIC_ROOT / "assets"
    if assets.is_dir():
        app.mount("/assets", StaticFiles(directory=str(assets)), name="assets")

    # HTML pages
    pages = {
        "/": "index.html",
        "/pricing": "pricing.html",
        "/checkout": "checkout.html",
        "/onboarding": "onboarding.html",
        "/investors": "investors.html",
        "/roadmap": "investors.html",
        "/metrics": "metrics.html",
        "/admin": "admin.html",
        "/contact": "contact.html",
        "/privacy": "privacy.html",
        "/terms": "terms.html",
        "/security-policy": "security-policy.html",
        "/status": "status.html",
        "/demo": "demo.html",
        "/faq": "faq.html",
    }

    for route, filename in pages.items():

        def make_handler(fn: str):
            async def handler():
                return _page(fn)

            return handler

        app.add_api_route(route, make_handler(filename), methods=["GET"], include_in_schema=False)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("unhandled_exception path=%s", request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error", "type": type(exc).__name__},
        )


app = create_app()
