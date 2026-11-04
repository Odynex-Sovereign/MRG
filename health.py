"""Liveness, readiness, and info endpoints."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from mrg import __version__
from mrg.config import get_settings

logger = logging.getLogger("mrg.health")
router = APIRouter(tags=["health"])


@router.get("/healthz", summary="Liveness probe")
async def liveness() -> dict[str, Any]:
    """Kubernetes / load-balancer liveness — process is up."""
    settings = get_settings()
    return {
        "status": "healthy",
        "engine": "MRG Planet-Scale Grid",
        "version": __version__,
        "environment": settings.environment,
    }


@router.get("/readyz", summary="Readiness probe")
async def readiness(request: Request) -> JSONResponse:
    """Readiness — dependencies required to serve traffic."""
    settings = get_settings()
    checks: dict[str, str] = {"app": "ok"}
    ready = True

    pool = getattr(request.app.state, "db_pool", None)
    if settings.has_database:
        if pool is None:
            checks["database"] = "unavailable"
            ready = False
        else:
            try:
                async with pool.acquire() as conn:
                    await conn.fetchval("SELECT 1")
                checks["database"] = "ok"
            except Exception as exc:
                logger.warning("readiness_db_check_failed: %s", exc)
                checks["database"] = "error"
                ready = False
    else:
        checks["database"] = "not_configured"

    checks["deepseek"] = "configured" if settings.has_deepseek else "sandbox"
    checks["nvidia"] = "configured" if settings.has_nvidia else "sandbox"

    status_code = 200 if ready else 503
    body = {
        "status": "ready" if ready else "not_ready",
        "checks": checks,
        "version": __version__,
    }
    return JSONResponse(content=body, status_code=status_code)


@router.get("/info", summary="Service metadata")
async def info() -> dict[str, Any]:
    settings = get_settings()
    return {
        "name": settings.app_name,
        "version": __version__,
        "environment": settings.environment,
        "sandbox_mode": not settings.has_deepseek,
        "features": {
            "billing": settings.enable_billing,
            "sensory": settings.enable_sensory,
            "database": settings.has_database,
        },
    }
