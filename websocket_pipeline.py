import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="MRG Crisis Simulation Grid - Premium Tier")

class SensoryPacket(BaseModel):
    haptic_frequency: float  
    haptic_intensity: float  
    scent_profile_id: str    
    concentration_ppm: float 

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
        if session_id in self.sensory_queues:
            try:
                self.sensory_queues[session_id].put_nowait(packet)
            except asyncio.QueueFull:
                pass 

manager = ConnectionManager()

async def sensory_streaming_worker(session_id: str, websocket: WebSocket):
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

@app.get("/")
async def root_health_check():
    return {"status": "healthy", "service": "MRG Engine Stack"}

@app.websocket("/ws/simulation/{session_id}")
async def websocket_simulation_endpoint(websocket: WebSocket, session_id: str, user_tier: str = "Standard"):
    await manager.connect(session_id, websocket, user_tier)
    
    worker_task = None
    if user_tier == "Premium_Research":
        worker_task = asyncio.create_task(sensory_streaming_worker(session_id, websocket))
        
    try:
        while True:
            data = await websocket.receive_json()
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
