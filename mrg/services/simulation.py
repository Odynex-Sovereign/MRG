import asyncio
import json
import random
from fastapi import WebSocket, WebSocketDisconnect

class SimulationStreamManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_telemetry(self, websocket: WebSocket):
        try:
            while True:
                payload = {
                    "telemetry": {"vocal_stress_index": round(random.uniform(5.0, 45.0), 2)},
                    "macroGrid": {"grid_stability_index": round(random.uniform(90.0, 99.8), 2)}
                }
                await websocket.send_text(json.dumps(payload))
                await asyncio.sleep(1.0)
        except (WebSocketDisconnect, Exception):
            self.disconnect(websocket)

stream_manager = SimulationStreamManager()
