import asyncio
from typing import Dict, Any
from pydantic import BaseModel

class SensoryVector(BaseModel):
    intensity: float
    duration_ms: int
    hardware_channel: str
    metadata: Dict[str, Any]

class SeamlessSensoryRouter:
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
                self.active_queues[session_id].put_nowait(vector)
            except asyncio.QueueFull:
                pass

    async def stream_worker(self, session_id: str, websocket_connection: Any):
        queue = self.active_queues.get(session_id)
        if not queue:
            return
            
        while session_id in self.active_queues:
            try:
                vector = await queue.get()
                await websocket_connection.send_json({
                    "type": "MULTI_SENSORY_TELEMETRY",
                    "payload": vector.model_dump()
                })
                queue.task_done()
            except Exception:
                break
