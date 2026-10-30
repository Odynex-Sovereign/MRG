"""
MRG Core Real-Time Simulation Orchestrator
Planet-scale crisis simulation WebSocket + REST entrypoint.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("MRG_Core_Pipeline")


class MacroState(BaseModel):
    brent_crude_price_usd: float = 84.50
    global_shipping_delay_pct: int = 22
    sovereign_bond_yield_basis_points: int = 420
    grid_stability_index: int = 95


class TelemetryPacket(BaseModel):
    user_id: str
    session_id: str
    vertical: str = Field(
        ...,
        description="One of: Corporate, Political, Healthcare, Veterinary, Industrial, "
        "Military, Aviation, Cyber, Geopolitical, Macro, Logistics, Higher-Ed, Asset-Defense",
    )
    vocal_pitch_variance: float = Field(ge=0.0, le=100.0)
    vocal_energy: float = Field(ge=0.0, le=100.0)
    response_latency_ms: int = Field(ge=0, le=5000)
    user_raw_text: str = ""


_db_pool = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _db_pool
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        try:
            import asyncpg
            _db_pool = await asyncpg.create_pool(db_url, min_size=2, max_size=10, command_timeout=5.0)
            logger.info("PostgreSQL pool ready")
        except Exception as e:
            logger.warning("DB pool unavailable (sandbox mode): %s", e)
            _db_pool = None
    else:
        logger.info("No DATABASE_URL — running in pure sandbox mode")
    yield
    if _db_pool:
        await _db_pool.close()


app = FastAPI(
    title="MRG Real-Time Simulation Orchestrator",
    description="Planet-scale crisis simulation grid powered by NVIDIA stack + DeepSeek",
    version="1.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def health_check():
    return {
        "status": "healthy",
        "engine": "ODYNEX_AXIS_LOGISTICS",
        "version": "1.1.0",
        "db_connected": _db_pool is not None,
        "nvidia_nim_configured": bool(os.getenv("NVIDIA_NIM_API_KEY")),
        "deepseek_configured": bool(os.getenv("DEEPSEEK_API_KEY")),
    }


@app.get("/")
async def root():
    return {
        "service": "MRG Crisis Simulation Grid",
        "docs": "/docs",
        "ws_endpoint": "/ws/simulation",
        "health": "/healthz",
    }


def compute_stress_index(packet: TelemetryPacket) -> int:
    return min(
        100,
        int(
            (packet.vocal_pitch_variance * 1.5)
            + (packet.vocal_energy * 0.8)
            + (packet.response_latency_ms / 50)
        ),
    )


def build_payload(packet: TelemetryPacket, stress_index: int) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "telemetry": {
            "vocal_stress_index": stress_index,
            "computed_physical_manifestation": int(stress_index * 0.9),
            "response_latency_ms": packet.response_latency_ms,
        },
        "macro_economic_grid": {
            "brent_crude_price_usd": 84.50,
            "global_shipping_delay_pct": 22,
            "sovereign_bond_yield_basis_points": 420,
            "grid_stability_index": max(0, 95 - int(stress_index * 0.15)),
        },
        "nvidia_audio2face_trigger": {
            "expression_profile": "calculated_neutral",
            "blendshape_intensity": round(min(1.0, stress_index / 100.0), 2),
        },
        "session": {
            "user_id": packet.user_id,
            "session_id": packet.session_id,
            "vertical": packet.vertical,
        },
    }

    vertical = packet.vertical.lower().replace(" ", "-")

    if vertical in ("higher-ed", "higher_ed", "youth"):
        payload["telemetry"].update(
            {
                "peer_pressure_resistance": max(0, 100 - int(stress_index * 1.1)),
                "rhetorical_defense_rating": min(
                    100, int((packet.response_latency_ms / 40) + (packet.vocal_energy * 0.9))
                ),
                "impostor_syndrome_resilience": max(0, 100 - stress_index),
            }
        )
        payload["nvidia_audio2face_trigger"]["expression_profile"] = "skeptical_brow_raise"

    elif vertical in ("asset-defense", "asset_defense", "corporate"):
        payload["telemetry"].update(
            {
                "tutsa_preemption_compliance": max(0, 100 - int(stress_index * 0.5)),
                "prior_art_validation_score": min(100, int(90 + (packet.vocal_energy * 0.2))),
                "generational_continuity_index": int(100 - (packet.response_latency_ms / 100)),
            }
        )
        payload["nvidia_audio2face_trigger"]["expression_profile"] = "calculated_protective"

    elif vertical in ("military", "tactical", "mil"):
        payload["telemetry"].update(
            {
                "roe_adherence": max(0, 100 - int(stress_index * 0.7)),
                "tactical_decisiveness": min(100, 100 - packet.response_latency_ms // 10),
                "vocal_control_under_stress": max(0, 100 - stress_index),
            }
        )
        payload["nvidia_audio2face_trigger"]["expression_profile"] = "command_focus"

    elif vertical in ("geopolitical", "diplomacy"):
        payload["telemetry"].update(
            {
                "strategic_ambiguity": min(100, int(70 + (100 - stress_index) * 0.3)),
                "diplomatic_leverage": max(0, 100 - stress_index),
                "treaty_alignment": max(0, 95 - int(stress_index * 0.4)),
            }
        )
        payload["nvidia_audio2face_trigger"]["expression_profile"] = "measured_restraint"

    elif vertical in ("macro", "central-banking", "banking"):
        payload["telemetry"].update(
            {
                "market_panic_containment": max(0, 100 - stress_index),
                "forward_guidance_clarity": min(100, 100 - packet.response_latency_ms // 8),
                "systemic_risk_mitigation": max(0, 90 - int(stress_index * 0.6)),
            }
        )
        payload["nvidia_audio2face_trigger"]["expression_profile"] = "calm_authority"

    return payload


@app.websocket("/ws/simulation")
async def simulation_stream_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Planetary Crisis Simulation link established.")

    try:
        while True:
            raw_data = await websocket.receive_text()
            try:
                data_json = json.loads(raw_data)
                packet = TelemetryPacket(**data_json)
            except Exception as e:
                await websocket.send_text(
                    json.dumps({"error": "invalid_packet", "detail": str(e)})
                )
                continue

            stress_index = compute_stress_index(packet)
            payload_out = build_payload(packet, stress_index)

            # Fire-and-forget viral roast when composure collapses
            if stress_index > 85:
                try:
                    from services.streaming.social_webhook import SocialAutomationHook

                    hook = SocialAutomationHook()
                    asyncio.create_task(
                        hook.broadcast_failed_challenge(
                            user_name=packet.user_id,
                            headline="Operational Grid Disruption",
                            score=100 - stress_index,
                            vertical=packet.vertical,
                        )
                    )
                except Exception as e:
                    logger.debug("Social hook skipped: %s", e)

            await websocket.send_text(json.dumps(payload_out))

    except WebSocketDisconnect:
        logger.warning("Crucible Edge link disconnected.")
    except Exception as e:
        logger.exception("Unexpected pipeline error: %s", e)
        try:
            await websocket.close(code=1011)
        except Exception:
            pass


# Include routers (auth, billing, keys) — safe import
try:
    from services.auth.routes import router as auth_router
    from services.auth.api_keys import router as api_keys_router
    from services.auth.billing import router as billing_router

    app.include_router(auth_router)
    app.include_router(api_keys_router)
    app.include_router(billing_router)
    logger.info("Auth / API-keys / Billing routers mounted")
except Exception as e:
    logger.warning("Optional routers not mounted: %s", e)
