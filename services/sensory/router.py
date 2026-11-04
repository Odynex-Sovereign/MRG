# services/sensory/router.py
import asyncio
from typing import Dict, Any, Optional
from pydantic import BaseModel

class SensoryVector(BaseModel):
    intensity: float
    duration_ms: int
    hardware_channel: str
    metadata: Dict[str, Any]

class SeamlessSensoryRouter:
    """
    Handles non-blocking multi-sensory message distribution across active client connections.
    """
    def __init__(self):
        self.active_queues: Dict[str, asyncio.Queue] = {}

    async def register_session(self, session_id: str):
        self.active_queues[session_id] = asyncio.Queue(maxsize=100)

    async def deregister_session(self, session_id: str):
        if session_id in self.active_queues:
            del self.active_queues[session_id]

    async def enqueue_telemetry(self, session_id: str, vector: SensoryVector):
        if session_id in self.active_queues:
            try:
                # Use nowait to guarantee zero blocking on the cognitive orchestrator
                self.active_queues[session_id].put_nowait(vector)
            except asyncio.QueueFull:
                # Drop frames gracefully if hardware connection experiences lag
                pass

    async def stream_worker(self, session_id: str, websocket_connection: Any):
        queue = self.active_queues.get(session_id)
        if not queue:
            return
            
        while session_id in self.active_queues:
            try:
                vector = await queue.get()
                # Broadcast payload formatted for Big Tech spatial runtimes (VisionOS / Presence Platform)
                await websocket_connection.send_json({
                    "type": "MULTI_SENSORY_TELEMETRY",
                    "payload": vector.model_dump()
                })
                queue.task_done()
            except Exception:
                break
