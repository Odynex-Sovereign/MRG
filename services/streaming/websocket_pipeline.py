import json
import logging
import os
import uuid
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

try:
    from sqlalchemy.orm import Session
except ImportError:  # A sandbox/startup environment may not have SQLAlchemy installed yet.
    Session = Any

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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mrg_pipeline")

app = FastAPI(title="MRG Integrated Simulation Suite", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Server-controlled catalog: clients choose a tier, never an amount or Stripe price.
CHECKOUT_TIERS = {
    "tier_1": {"name": "Molecular SaaS", "amount": 1_500_000},
    "tier_2": {"name": "Infrastructure Base", "amount": 3_500_000},
    "tier_3": {"name": "Platinum CAVE", "amount": 16_000_000},
}


class CheckoutRequest(BaseModel):
    session_id: str | None = Field(default=None, min_length=1, max_length=100)
    tier_id: str = Field(min_length=1, max_length=40)


@app.get("/", include_in_schema=False)
async def homepage():
    """Serve the browser UI instead of returning health JSON at the site root."""
    index_file = Path(__file__).resolve().parents[2] / "index.html"
    return FileResponse(index_file, media_type="text/html")


@app.get("/healthz")
async def health_check():
    """Liveness endpoint used by Fly.io and deployment checks."""
    return {
        "status": "healthy",
        "engine": "MRG Planet-Scale Grid",
        "mode": "live" if os.getenv("STRIPE_SECRET_KEY") else "sandbox",
        "billing_configured": bool(os.getenv("STRIPE_SECRET_KEY")),
    }


@app.post("/billing/v1/checkout/create-session")
async def create_checkout_session(payload: CheckoutRequest, request: Request):
    """Create a Stripe-hosted monthly subscription checkout session."""
    tier = CHECKOUT_TIERS.get(payload.tier_id)
    if tier is None:
        raise HTTPException(status_code=400, detail="Unknown checkout tier.")

    stripe_key = os.getenv("STRIPE_SECRET_KEY")
    if not stripe_key:
        return {
            "mode": "sandbox",
            "checkout_url": None,
            "error": "stripe_not_configured",
            "message": "Stripe is not configured on this server. No charge was attempted.",
        }

    try:
        import stripe
    except ImportError as exc:
        logger.exception("Stripe SDK is missing while billing is configured")
        raise HTTPException(status_code=503, detail="Stripe checkout is unavailable.") from exc

    base_url = os.getenv("PUBLIC_BASE_URL", "https://mrg.fly.dev").rstrip("/")
    client_reference = payload.session_id or f"mrg_{uuid.uuid4().hex}"
    try:
        stripe.api_key = stripe_key
        session = stripe.checkout.Session.create(
            mode="subscription",
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": tier["name"]},
                        "unit_amount": tier["amount"],
                        "recurring": {"interval": "month"},
                    },
                    "quantity": 1,
                }
            ],
            client_reference_id=client_reference,
            metadata={"tier_id": payload.tier_id},
            success_url=f"{base_url}/?checkout=success&session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{base_url}/?checkout=cancelled#pricing",
        )
    except Exception as exc:
        # Do not expose provider errors or credentials in API responses.
        logger.exception("Stripe Checkout session creation failed for tier %s", payload.tier_id)
        raise HTTPException(
            status_code=502,
            detail="Stripe could not start checkout. Please try again or contact support.",
        ) from exc

    return {
        "mode": "live",
        "checkout_url": session.url,
        "session_id": session.id,
    }


@app.websocket("/ws/simulation")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        await websocket.send_json({
            "type": "SYSTEM_STATUS",
            "payload": {"message": "Connected to the MRG simulation service."},
        })
        while True:
            raw_message = await websocket.receive_text()
            try:
                payload = json.loads(raw_message)
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "SYSTEM_ERROR",
                    "payload": {"message": "Invalid JSON frame received."},
                })
                continue

            action = payload.get("action", "")
            if action != "TRIGGER_CRISIS":
                await websocket.send_json({
                    "type": "SYSTEM_ERROR",
                    "payload": {"message": f"Unknown execution target: {action}"},
                })
                continue

            prompt = str(payload.get("prompt", ""))
            try:
                macro_response = await generate_macro_ripple(prompt)
                await websocket.send_json({
                    "type": "MACRO_COGNITIVE_UPDATE",
                    "payload": {"analysis": macro_response},
                })
                audio_bytes = await synthesize_speech_stream(macro_response[:200])
                await websocket.send_json({
                    "type": "SENSORY_STREAM_INFO",
                    "payload": {"audio_chunk_size": len(audio_bytes), "status": "streaming"},
                })
            except Exception:
                logger.exception("Simulation request failed")
                await websocket.send_json({
                    "type": "SYSTEM_ERROR",
                    "payload": {"message": "Simulation request failed; check application logs."},
                })
    except WebSocketDisconnect:
        pass
    except Exception:
        logger.exception("WebSocket pipeline failed")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "services.streaming.websocket_pipeline:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
