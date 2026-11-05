"""MRG production entrypoint used by Docker / Fly.

Serves the institutional allocation UI, health checks, WebSocket simulation
channel, and the billing checkout API.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

try:
    from sqlalchemy.orm import Session
except ImportError:
    Session = Any  # type: ignore[misc, assignment]

# Optional infrastructure integrations must not prevent sandbox startup.
try:
    from db_client import get_db
except ImportError:

    def get_db():
        yield None


try:
    from deepseek_client import generate_macro_ripple
except ImportError:

    async def generate_macro_ripple(prompt: str) -> str:
        return f"[Sandbox mode] Simulating systemic macro effects for: {prompt}"


try:
    from riva_tts import synthesize_speech_stream
except ImportError:

    async def synthesize_speech_stream(text: str) -> bytes:
        return b"MOCK_WAV_AUDIO_STREAM_DATA"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("mrg_pipeline")

app = FastAPI(title="MRG Integrated Simulation Suite", version="1.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )
        return response


app.add_middleware(SecurityHeadersMiddleware)


@app.on_event("startup")
async def startup_event():
    logger.info("MRG simulation service started")


@app.get("/", include_in_schema=False)
async def homepage():
    """Serve the browser UI instead of returning health JSON at the site root."""
    index_file = Path(__file__).resolve().parents[2] / "index.html"
    return FileResponse(index_file, media_type="text/html")


@app.get("/healthz")
@app.get("/health")
async def health_check():
    """Liveness / readiness endpoint used by Fly.io and deployment checks."""
    stripe_ok = bool(
        __import__("os").getenv("STRIPE_SECRET_KEY")
        or __import__("os").getenv("STRIPE_API_KEY")
    )
    return {
        "status": "healthy",
        "engine": "MRG Planet-Scale Grid",
        "mode": "resilient_boot",
        "billing_configured": stripe_ok,
    }


# Register checkout router (path: /billing/v1/checkout/create-session)
try:
    from checkout_engine import router as checkout_router

    app.include_router(checkout_router)
    logger.info("Checkout router registered at /billing/v1/checkout")
except Exception as exc:  # noqa: BLE001
    logger.exception("Failed to register checkout router: %s", exc)


class SimulationConnectionManager:
    """Tracks active simulation WebSocket connections."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(
            "Simulation connection accepted; active=%d", len(self.active_connections)
        )

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(
                "Simulation connection closed; active=%d", len(self.active_connections)
            )


manager = SimulationConnectionManager()


@app.websocket("/ws/simulation")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        await websocket.send_json(
            {
                "type": "SYSTEM_STATUS",
                "payload": {"message": "Connected to the MRG simulation service."},
            }
        )
        while True:
            raw_message = await websocket.receive_text()
            try:
                payload = json.loads(raw_message)
            except json.JSONDecodeError:
                await websocket.send_json(
                    {
                        "type": "SYSTEM_ERROR",
                        "payload": {"message": "Invalid JSON frame received."},
                    }
                )
                continue

            action = payload.get("action", "")
            if action != "TRIGGER_CRISIS":
                await websocket.send_json(
                    {
                        "type": "SYSTEM_ERROR",
                        "payload": {"message": f"Unknown execution target: {action}"},
                    }
                )
                continue

            prompt = str(payload.get("prompt", ""))
            try:
                macro_response = await generate_macro_ripple(prompt)
                await websocket.send_json(
                    {
                        "type": "MACRO_COGNITIVE_UPDATE",
                        "payload": {"analysis": macro_response},
                    }
                )
                audio_bytes = await synthesize_speech_stream(macro_response[:200])
                await websocket.send_json(
                    {
                        "type": "SENSORY_STREAM_INFO",
                        "payload": {
                            "audio_chunk_size": len(audio_bytes),
                            "status": "streaming",
                        },
                    }
                )
            except Exception:
                logger.exception("Simulation request failed")
                await websocket.send_json(
                    {
                        "type": "SYSTEM_ERROR",
                        "payload": {
                            "message": "Simulation request failed; check application logs."
                        },
                    }
                )
    except WebSocketDisconnect:
        pass
    except Exception:
        logger.exception("WebSocket pipeline failed")
    finally:
        manager.disconnect(websocket)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    logger.exception("unhandled_exception path=%s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": type(exc).__name__},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "services.streaming.websocket_pipeline:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
