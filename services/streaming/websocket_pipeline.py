import asyncio
import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MRG_Core_Pipeline")

app = FastAPI(title="MRG Real-Time Simulation Orchestrator")


class MacroState(BaseModel):
    brent_crude_price_usd: float
    global_shipping_delay_pct: int
    sovereign_bond_yield_basis_points: int
    grid_stability_index: int


class TelemetryPacket(BaseModel):
    user_id: str
    session_id: str
    vertical: str
    vocal_pitch_variance: float
    vocal_energy: float
    response_latency_ms: int
    user_raw_text: str


@app.get("/healthz")
async def health_check():
    return {"status": "healthy", "engine": "ODYNEX_AXIS_LOGISTICS"}


@app.websocket("/ws/simulation")
async def simulation_stream_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Planetary Crisis Simulation link established.")

    try:
        while True:
            raw_data = await websocket.receive_text()
            data_json = json.loads(raw_data)
            packet = TelemetryPacket(**data_json)

            pitch_var = packet.vocal_pitch_variance
            energy = packet.vocal_energy
            stress_index = min(
                100, int((pitch_var * 1.5) + (energy * 0.8) + (packet.response_latency_ms / 50))
            )

            payload_out = {
                "telemetry": {
                    "vocal_stress_index": stress_index,
                    "computed_physical_manifestation": int(stress_index * 0.9),
                },
                "macro_economic_grid": {
                    "brent_crude_price_usd": 84.50,
                    "global_shipping_delay_pct": 22,
                    "sovereign_bond_yield_basis_points": 420,
                    "grid_stability_index": 95,
                },
                "nvidia_audio2face_trigger": {
                    "expression_profile": "calculated_neutral",
                    "blendshape_intensity": round(min(1.0, stress_index / 100.0), 2),
                },
            }

            if packet.vertical == "Higher-Ed":
                payload_out["telemetry"].update(
                    {
                        "peer_pressure_resistance": max(0, 100 - int(stress_index * 1.1)),
                        "rhetorical_defense_rating": min(
                            100,
                            int((packet.response_latency_ms / 40) + (energy * 0.9)),
                        ),
                    }
                )
                payload_out["nvidia_audio2face_trigger"]["expression_profile"] = "skeptical_brow_raise"

            elif packet.vertical == "Asset-Defense":
                payload_out["telemetry"].update(
                    {
                        "tutsa_preemption_compliance": max(0, 100 - int(stress_index * 0.5)),
                        "prior_art_validation_score": min(100, int(90 + (energy * 0.2))),
                        "generational_continuity_index": int(100 - (packet.response_latency_ms / 100)),
                    }
                )
                payload_out["nvidia_audio2face_trigger"]["expression_profile"] = "calculated_protective"

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
