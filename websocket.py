"""WebSocket simulation pipeline."""

from __future__ import annotations

import json
import logging
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ValidationError, field_validator

from mrg.config import get_settings
from mrg.services.macro import generate_macro_ripple
from mrg.services.sensory import synthesize_speech_stream

logger = logging.getLogger("mrg.websocket")
router = APIRouter(tags=["simulation"])


class TelemetryPacket(BaseModel):
    """Client telemetry / crisis trigger payload."""

    user_id: str | None = None
    session_id: str | None = None
    vertical: str | None = None
    vocal_pitch_variance: float | None = None
    vocal_energy: float | None = None
    response_latency_ms: float | None = None
    user_raw_text: str | None = None
    action: str | None = None
    prompt: str | None = None

    @field_validator("user_raw_text", "prompt", mode="before")
    @classmethod
    def truncate_text(cls, v: Any) -> Any:
        if isinstance(v, str) and len(v) > 4000:
            return v[:4000]
        return v


class ConnectionManager:
    """Track active simulation WebSocket connections."""

    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("ws_connected active=%d", len(self.active_connections))

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info("ws_disconnected active=%d", len(self.active_connections))

    @property
    def count(self) -> int:
        return len(self.active_connections)


manager = ConnectionManager()


@router.websocket("/ws/simulation")
async def websocket_simulation(websocket: WebSocket) -> None:
    """Primary simulation channel.

    Accepts either:
    - Telemetry packets (vertical, vocal metrics, user_raw_text)
    - Explicit {"action": "TRIGGER_CRISIS", "prompt": "..."} frames
    """
    settings = get_settings()
    await manager.connect(websocket)

    try:
        await websocket.send_json(
            {
                "type": "SYSTEM_STATUS",
                "payload": {
                    "message": "Connected to the MRG simulation service.",
                    "version": settings.app_version,
                    "sandbox": not settings.has_deepseek,
                },
            }
        )

        while True:
            raw = await websocket.receive_text()
            if len(raw.encode("utf-8")) > settings.max_message_size_bytes:
                await websocket.send_json(
                    {
                        "type": "SYSTEM_ERROR",
                        "payload": {"message": "Message exceeds size limit."},
                    }
                )
                continue

            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json(
                    {
                        "type": "SYSTEM_ERROR",
                        "payload": {"message": "Invalid JSON frame received."},
                    }
                )
                continue

            try:
                packet = TelemetryPacket.model_validate(data)
            except ValidationError as exc:
                await websocket.send_json(
                    {
                        "type": "SYSTEM_ERROR",
                        "payload": {
                            "message": "Payload validation failed.",
                            "errors": exc.errors(),
                        },
                    }
                )
                continue

            prompt = (packet.prompt or packet.user_raw_text or "").strip()
            action = (packet.action or "").upper()

            # Accept telemetry-style packets and explicit crisis triggers
            if not prompt and action != "TRIGGER_CRISIS":
                await websocket.send_json(
                    {
                        "type": "SYSTEM_ERROR",
                        "payload": {
                            "message": "Provide user_raw_text, prompt, or action=TRIGGER_CRISIS.",
                        },
                    }
                )
                continue

            if not prompt:
                prompt = "Initiate baseline crisis scenario."

            try:
                context = {
                    "vertical": packet.vertical,
                    "session_id": packet.session_id,
                    "vocal_energy": packet.vocal_energy,
                    "vocal_pitch_variance": packet.vocal_pitch_variance,
                    "response_latency_ms": packet.response_latency_ms,
                }
                macro_response = await generate_macro_ripple(prompt, context)
                await websocket.send_json(
                    {
                        "type": "MACRO_COGNITIVE_UPDATE",
                        "payload": {
                            "analysis": macro_response,
                            "vertical": packet.vertical,
                            "session_id": packet.session_id,
                        },
                    }
                )

                if settings.enable_sensory:
                    audio_bytes = await synthesize_speech_stream(str(macro_response)[:200])
                    await websocket.send_json(
                        {
                            "type": "SENSORY_STREAM_INFO",
                            "payload": {
                                "audio_chunk_size": len(audio_bytes),
                                "status": "streaming" if audio_bytes else "skipped",
                            },
                        }
                    )
            except Exception:
                logger.exception("simulation_request_failed")
                await websocket.send_json(
                    {
                        "type": "SYSTEM_ERROR",
                        "payload": {
                            "message": "Simulation request failed; check application logs.",
                        },
                    }
                )

    except WebSocketDisconnect:
        logger.debug("client_disconnected")
    except Exception:
        logger.exception("websocket_pipeline_error")
    finally:
        manager.disconnect(websocket)
