from __future__ import annotations

import asyncio
from typing import Any, AsyncIterator

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from mrg import __version__
from mrg.config import Settings, get_settings


async def run_sandbox_simulation(session: Any, scenario_id: str) -> AsyncIterator[dict[str, Any]]:
    """Yield scenario events for a sandboxed simulation run."""
    yield {"type": "scenario_start", "scenario": scenario_id}
    await asyncio.sleep(0)
    yield {
        "type": "scenario_complete",
        "metrics": {"composure_score": 80},
        "debrief": "Scenario completed successfully.",
    }


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description=(
            "Planet-scale crisis simulation grid combining macro structural reasoning, "
            "low-latency micro-conversational avatars, and sensory engines."
        ),
    )

    app.state.settings = settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    @app.get("/readyz")
    async def readyz() -> dict[str, str]:
        return {"status": "ready", "version": __version__}

    @app.get("/api/version")
    async def api_version() -> dict[str, str]:
        return {"version": __version__}

    @app.get("/api/pricing")
    async def api_pricing() -> dict[str, Any]:
        return {
            "currency": "USD",
            "plans": [
                {"name": "Starter", "price": 0, "description": "Sandbox access"},
                {"name": "Executive", "price": 49, "description": "Scenario library"},
                {"name": "Enterprise", "price": 199, "description": "Team and institutional access"},
            ],
        }

    @app.post("/api/feedback")
    async def api_feedback(payload: dict[str, Any]) -> dict[str, Any]:
        message = str(payload.get("message") or "Feedback submitted")
        return {"status": "received", "message": message}

    @app.websocket("/ws/simulation")
    async def websocket_simulation(websocket: WebSocket):
        await websocket.accept()
        await websocket.send_json({"type": "SYSTEM_STATUS"})

        while True:
            try:
                payload = await websocket.receive_json()
            except WebSocketDisconnect:
                break
            except ValueError:
                continue

            action = str(payload.get("action") or "").upper()
            if action == "START":
                scenario = str(payload.get("scenario") or "macro_shock")
                async for event in run_sandbox_simulation(websocket, scenario):
                    await websocket.send_json(event)
                continue

            if action == "TRIGGER_CRISIS":
                prompt = str(payload.get("prompt") or "test incident")
                await websocket.send_json({
                    "type": "MACRO_COGNITIVE_UPDATE",
                    "message": f"Crisis trigger received: {prompt}",
                    "prompt": prompt,
                })
                await websocket.send_json({
                    "type": "SENSORY_STREAM_INFO",
                    "stream": "macro",
                    "status": "active",
                    "prompt": prompt,
                })
                continue

            await websocket.send_json({"type": "SYSTEM_STATUS", "message": "Unsupported action"})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request, exc: Exception):
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    return app


app = create_app()
