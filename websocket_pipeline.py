# services/streaming/websocket_pipeline.py
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, Any
from pydantic import BaseModel

app = FastAPI(title="MRG Crisis Simulation Grid - Premium Tier")

# Define the sensory structure expected by Apple VisionOS / Meta Presence Platform SDK shims
class SensoryPacket(BaseModel):
    haptic_frequency: float  # Hz (0.0 to 250.0)
    haptic_intensity: float  # Amplitude (0.0 to 1.0)
    scent_profile_id: str    # Universal Scent Manifest Matrix ID
    concentration_ppm: float # Scent saturation density

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.sensory_queues: Dict[str, asyncio.Queue] = {}

    async def connect(self, session_id: str, websocket: WebSocket, user_tier: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        if user_tier == "Premium_Research":
            self.sensory_queues[session_id] = asyncio.Queue(maxsize=150)

    def disconnect(self, session_id: str):
        self.active_connections.pop(session_id, None)
        self.sensory_queues.pop(session_id, None)

    async def push_sensory(self, session_id: str, packet: SensoryPacket):
        # Enqueue sensory data asynchronously without blocking the cognitive loops
        if session_id in self.sensory_queues:
            try:
                self.sensory_queues[session_id].put_nowait(packet)
            except asyncio.QueueFull:
                pass # Gracefully drop overflow packets if hardware channel experiences jitter

manager = ConnectionManager()

async def sensory_streaming_worker(session_id: str, websocket: WebSocket):
    """
    Dedicated worker that unloads sensory metrics from the queue 
    and broadcasts them to the spatial computing client.
    """
    queue = manager.sensory_queues.get(session_id)
    if not queue:
        return
    try:
        while True:
            packet = await queue.get()
            await websocket.send_json({
                "event": "SENSORY_TELEMETRY",
                "data": packet.model_dump()
            })
            queue.task_done()
    except (WebSocketDisconnect, asyncio.CancelledError):
        pass

@app.websocket("/ws/simulation/{session_id}")
async def websocket_simulation_endpoint(websocket: WebSocket, session_id: str, user_tier: str = "Standard"):
    await manager.connect(session_id, websocket, user_tier)
    
    # Spawn background task for multi-sensory telemetry if premium
    worker_task = None
    if user_tier == "Premium_Research":
        worker_task = asyncio.create_task(sensory_streaming_worker(session_id, websocket))
        
    try:
        while True:
            # Handle inbound control frames or mic streaming from standard client pipeline
            data = await websocket.receive_json()
            
            # --- Simulated Cognitive/Sensory Loop Internal Trigger ---
            # If system detects a physical crisis event, calculate metrics and push:
            if data.get("action") == "trigger_crisis_event":
                mock_packet = SensoryPacket(
                    haptic_frequency=145.5,
                    haptic_intensity=0.85,
                    scent_profile_id=data.get("scent_trigger", "NONE"),
                    concentration_ppm=12.5
                )
                await manager.push_sensory(session_id, mock_packet)
                
    except WebSocketDisconnect:
        manager.disconnect(session_id)
        if worker_task:
            worker_task.cancel()
