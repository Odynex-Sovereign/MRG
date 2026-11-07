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
        """Generates real-time synthetic crisis matrices simulating executive pressure."""
        vocal_stress = 12.0
        shipping_delay = 22.0
        grid_stability = 95.0
        
        try:
            while True:
                # Add micro-fluctuations to mimic streaming sensor digital twins
                vocal_stress = max(0.0, min(100.0, vocal_stress + random.uniform(-2.5, 3.0)))
                shipping_delay = max(0.0, min(100.0, shipping_delay + random.uniform(-0.5, 0.6)))
                grid_stability = max(0.0, min(100.0, grid_stability + random.uniform(-1.0, 0.9)))

                payload = {
                    "telemetry": {
                        "vocal_stress_index": round(vocal_stress, 2),
                        "tutsa_preemption_compliance": round(random.uniform(94.0, 100.0), 2),
                        "prior_art_validation_score": int(random.randint(98, 100)),
                        "generational_continuity_index": round(random.uniform(99.1, 100.0), 2)
                    },
                    "macroGrid": {
                        "brent_crude_price_usd": round(84.5 + random.uniform(-1.2, 1.5), 2),
                        "global_shipping_delay_pct": round(shipping_delay, 2),
                        "grid_stability_index": round(grid_stability, 2)
                    }
                }
                
                await websocket.send_text(json.dumps(payload))
                await asyncio.sleep(1.0)  # Stream frequency update tick (1Hz)
                
        except WebSocketDisconnect:
            self.disconnect(websocket)
        except Exception as e:
            print(f"Telemetry broadcasting intercept: {e}")
            self.disconnect(websocket)

stream_manager = SimulationStreamManager()
