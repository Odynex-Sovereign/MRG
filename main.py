"""MRG Integrated Simulation Suite — serves complete static HTML pages + API + WebSocket."""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from mrg import __version__
from mrg.core.config import get_settings
from mrg.core.pricing import INSTITUTIONAL_RANGES, list_public_plans
from mrg.core.security import RateLimitMiddleware, SecurityHeadersMiddleware, SimpleRateLimiter
from mrg.services.simulation import SimulationSession, run_sandbox_simulation

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
logger = logging.getLogger("mrg")


def _resolve_root() -> Path:
    for c in (Path(__file__).resolve().parents[1], Path.cwd(), Path(os.environ.get("MRG_ROOT", ""))):
        if c and (c / "static").is_dir():
            return c
    return Path(__file__).resolve().parents[1]


ROOT = _resolve_root()
STATIC_DIR = ROOT / "static"
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "Starting MRG v%s env=%s root=%s static=%s index=%s",
        __version__,
        settings.environment,
        ROOT,
        STATIC_DIR.is_dir(),
        (STATIC_DIR / "index.html").is_file(),
    )
    yield
    logger.info("Shutting down MRG")


app = FastAPI(
    title=settings.app_name,
    version=__version__,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url=None,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=["*"],
)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, limiter=SimpleRateLimiter(settings.rate_limit_rpm))

if STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _html(name: str):
    path = STATIC_DIR / name
    if path.is_file():
        return FileResponse(path, media_type="text/html; charset=utf-8")
    alt = ROOT / name
    if alt.is_file():
        return FileResponse(alt, media_type="text/html; charset=utf-8")
    return HTMLResponse(
        "<!DOCTYPE html><html><body style='background:#0a0c10;color:#e8ecf4;font-family:system-ui;padding:2rem'>"
        f"<h1>Missing {name}</h1><p>Redeploy the full package including static/.</p>"
        "<p><a href='/' style='color:#ff6b1a'>Home</a></p></body></html>",
        status_code=404,
    )


def _health_body():
    return {
        "status": "ok",
        "version": __version__,
        "environment": settings.environment,
        "engine": "MRG Integrated Simulation Suite",
        "mode": "sandbox" if not settings.deepseek_configured else "live-models",
        "billing_configured": settings.billing_configured,
    }


@app.api_route("/healthz", methods=["GET", "HEAD"], include_in_schema=False)
@app.api_route("/livez", methods=["GET", "HEAD"], include_in_schema=False)
async def healthz():
    return _health_body()


@app.api_route("/readyz", methods=["GET", "HEAD"], include_in_schema=False)
async def readyz():
    return {
        "status": "ready",
        "version": __version__,
        "billing_configured": settings.billing_configured,
        "websocket_enabled": settings.enable_websocket_simulation,
        "static_ok": STATIC_DIR.is_dir(),
        "index_ok": (STATIC_DIR / "index.html").is_file(),
    }


@app.get("/api/pricing")
async def api_pricing():
    return {
        "currency": "USD",
        "plans": list_public_plans(),
        "institutional_ranges": INSTITUTIONAL_RANGES,
        "notes": ["Prices are illustrative.", "Taxes may apply.", "Enterprise terms require written agreement."],
    }


@app.get("/api/version")
async def api_version():
    return {"version": __version__, "name": settings.app_name}


@app.post("/api/feedback")
async def api_feedback(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"detail": "Invalid JSON"}, status_code=400)
    message = str(body.get("message", ""))[:2000]
    if not message.strip():
        return JSONResponse({"detail": "Message is required"}, status_code=400)
    logger.info("Feedback len=%d", len(message))
    return {"status": "received", "message": "Thank you. We review feedback regularly."}


@app.websocket("/ws/simulation")
async def ws_simulation(websocket: WebSocket):
    if not settings.enable_websocket_simulation:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    session = SimulationSession()
    try:
        await websocket.send_json({"type": "welcome", "message": 'Send {"action": "start"}.'})
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            if action == "start":
                async for event in run_sandbox_simulation(session, data.get("scenario", "black_swan_supply")):
                    await websocket.send_json(event)
            elif action == "ping":
                await websocket.send_json({"type": "pong"})
            elif action == "stop":
                await websocket.send_json({"type": "stopped"})
                break
            else:
                await websocket.send_json({"type": "error", "message": "Unknown action."})
    except WebSocketDisconnect:
        pass
    except Exception as exc:
        logger.exception("WebSocket error: %s", exc)
        try:
            await websocket.close(code=1011)
        except Exception:
            pass


@app.get("/")
async def home():
    return _html("index.html")


@app.get("/pricing")
async def pricing_page():
    return _html("pricing.html")


@app.get("/institutions")
async def institutions_page():
    return _html("institutions.html")


@app.get("/demo")
async def demo_page():
    return _html("demo.html")


@app.get("/onboarding")
async def onboarding_page():
    return _html("onboarding.html")


@app.get("/dashboard")
async def dashboard_page():
    return _html("dashboard.html")


@app.get("/faq")
async def faq_page():
    return _html("faq.html")


@app.get("/security")
async def security_page():
    return _html("security.html")


@app.get("/accessibility")
async def accessibility_page():
    return _html("accessibility.html")


@app.get("/contact")
async def contact_page():
    return _html("contact.html")


@app.get("/legal/terms")
async def terms_page():
    return _html("legal_terms.html")


@app.get("/legal/privacy")
async def privacy_page():
    return _html("legal_privacy.html")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    path = STATIC_DIR / "icons" / "favicon.svg"
    if path.exists():
        return FileResponse(path, media_type="image/svg+xml")
    return Response(status_code=204)
