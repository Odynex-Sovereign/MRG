"""
MRG Integrated Simulation Suite — application entrypoint.
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from mrg import __version__
from mrg.core.config import get_settings
from mrg.core.pricing import INSTITUTIONAL_RANGES, list_public_plans
from mrg.core.security import RateLimitMiddleware, SecurityHeadersMiddleware, SimpleRateLimiter
from mrg.services.simulation import SimulationSession, run_sandbox_simulation

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("mrg")


def _resolve_root() -> Path:
    """Locate project root containing templates/ and static/."""
    candidates = [
        Path(__file__).resolve().parents[1],  # package parent (dev + Docker /app)
        Path.cwd(),
        Path(os.environ.get("MRG_ROOT", "")),
    ]
    for c in candidates:
        if c and (c / "templates").is_dir() and (c / "static").is_dir():
            return c
    # Fall back to package parent even if dirs missing (will error clearly at render)
    return Path(__file__).resolve().parents[1]


ROOT = _resolve_root()
STATIC_DIR = ROOT / "static"
TEMPLATES_DIR = ROOT / "templates"

settings = get_settings()

if not TEMPLATES_DIR.is_dir():
    logger.error("Templates directory missing: %s", TEMPLATES_DIR)
if not STATIC_DIR.is_dir():
    logger.error("Static directory missing: %s", STATIC_DIR)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "Starting MRG v%s env=%s root=%s billing=%s templates=%s",
        __version__,
        settings.environment,
        ROOT,
        settings.billing_configured,
        TEMPLATES_DIR.is_dir(),
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


# ---------------------------------------------------------------------------
# Health & readiness (GET + HEAD for Fly / load balancers)
# ---------------------------------------------------------------------------

def _health_body() -> dict:
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
        "deepseek_configured": settings.deepseek_configured,
        "websocket_enabled": settings.enable_websocket_simulation,
        "templates_ok": TEMPLATES_DIR.is_dir(),
        "static_ok": STATIC_DIR.is_dir(),
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

@app.get("/api/pricing")
async def api_pricing():
    return {
        "currency": "USD",
        "plans": list_public_plans(),
        "institutional_ranges": INSTITUTIONAL_RANGES,
        "notes": [
            "Prices are illustrative and subject to change.",
            "Taxes and payment-processor fees may apply.",
            "Nonprofit/Education requires verification.",
            "Enterprise and institutional buy-out terms are subject to written agreement.",
        ],
    }


@app.get("/api/version")
async def api_version():
    return {"version": __version__, "name": settings.app_name}


@app.post("/api/feedback")
async def api_feedback(request: Request):
    """Lightweight feedback endpoint — stores nothing sensitive by default."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"detail": "Invalid JSON"}, status_code=400)
    message = str(body.get("message", ""))[:2000]
    email = str(body.get("email", ""))[:200]
    category = str(body.get("category", "general"))[:40]
    if not message.strip():
        return JSONResponse({"detail": "Message is required"}, status_code=400)
    logger.info(
        "Feedback received category=%s email=%s len=%d",
        category,
        bool(email),
        len(message),
    )
    return {"status": "received", "message": "Thank you. We review feedback regularly."}


# ---------------------------------------------------------------------------
# WebSocket simulation (sandbox)
# ---------------------------------------------------------------------------

@app.websocket("/ws/simulation")
async def ws_simulation(websocket: WebSocket):
    if not settings.enable_websocket_simulation:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    session = SimulationSession()
    try:
        await websocket.send_json(
            {
                "type": "welcome",
                "message": 'MRG simulation channel ready. Send {"action": "start"}.',
            }
        )
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            if action == "start":
                scenario = data.get("scenario", "black_swan_supply")
                async for event in run_sandbox_simulation(session, scenario):
                    await websocket.send_json(event)
            elif action == "ping":
                await websocket.send_json({"type": "pong"})
            elif action == "stop":
                await websocket.send_json({"type": "stopped"})
                break
            else:
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Unknown action. Use start, ping, or stop.",
                    }
                )
    except WebSocketDisconnect:
        logger.debug("WebSocket client disconnected")
    except Exception as exc:
        logger.exception("WebSocket error: %s", exc)
        try:
            await websocket.close(code=1011)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# HTML pages
# ---------------------------------------------------------------------------

def _page(request: Request, name: str, **ctx):
    if not TEMPLATES_DIR.is_dir():
        return HTMLResponse(
            "<h1>MRG misconfigured</h1><p>Templates directory not found. "
            "Deploy the full package (templates/ and static/ next to the app).</p>",
            status_code=500,
        )
    return templates.TemplateResponse(
        request,
        name,
        {
            "app_name": settings.app_name,
            "version": __version__,
            "public_base_url": settings.public_base_url,
            "environment": settings.environment,
            **ctx,
        },
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return _page(request, "index.html", plans=list_public_plans())


@app.get("/pricing", response_class=HTMLResponse)
async def pricing_page(request: Request):
    return _page(request, "pricing.html", plans=list_public_plans())


@app.get("/institutions", response_class=HTMLResponse)
async def institutions_page(request: Request):
    return _page(
        request,
        "institutions.html",
        ranges=INSTITUTIONAL_RANGES,
        plans=list_public_plans(),
    )


@app.get("/demo", response_class=HTMLResponse)
async def demo_page(request: Request):
    return _page(request, "demo.html")


@app.get("/onboarding", response_class=HTMLResponse)
async def onboarding_page(request: Request):
    return _page(request, "onboarding.html")


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return _page(request, "dashboard.html")


@app.get("/faq", response_class=HTMLResponse)
async def faq_page(request: Request):
    return _page(request, "faq.html")


@app.get("/security", response_class=HTMLResponse)
async def security_page(request: Request):
    return _page(request, "security.html")


@app.get("/accessibility", response_class=HTMLResponse)
async def accessibility_page(request: Request):
    return _page(request, "accessibility.html")


@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    return _page(request, "contact.html")


@app.get("/legal/terms", response_class=HTMLResponse)
async def terms_page(request: Request):
    return _page(request, "legal_terms.html")


@app.get("/legal/privacy", response_class=HTMLResponse)
async def privacy_page(request: Request):
    return _page(request, "legal_privacy.html")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    path = STATIC_DIR / "icons" / "favicon.svg"
    if path.exists():
        return FileResponse(path, media_type="image/svg+xml")
    return Response(status_code=204)


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s: %s", request.url.path, exc)
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            {"detail": "An unexpected error occurred. Please try again later."},
            status_code=500,
        )
    return JSONResponse(
        {"detail": "An unexpected error occurred."},
        status_code=500,
    )
