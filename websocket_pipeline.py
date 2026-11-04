# services/streaming/websocket_pipeline.py
import os
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="MRG Crisis Simulation Stream Engine",
    version="1.0.0",
    lifespan=None # Handled via standard DB pools if needed
)

# CORS Middleware configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationState(BaseModel):
    session_id: str
    vertical: str
    composure_score: float

@app.get("/healthz")
async def health_check():
    return {"status": "healthy", "engine": "online", "sandbox": True}

@app.websocket("/ws/simulation/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        # Initial greeting payload
        await websocket.send_json({
            "event": "connected",
            "session_id": session_id,
            "message": "Successfully attached to planet-scale crisis matrix."
        })
        
        while True:
            # Await incoming telemetry stream (Vocal stress indices / Blendshapes)
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            # Extract metrics for behavior analysis
            vocal_stress = payload.get("vocal_stress", 0.0)
            decision_velocity = payload.get("decision_velocity", 1.0)
            
            # Simple algorithmic behavior model logic fallback
            composure_index = max(0.0, min(100.0, 100.0 - (vocal_stress * 50.0) - (decision_velocity * 2.0)))
            
            # Broadcast the updated system ripple state back to digital twin
            await websocket.send_json({
                "event": "telemetry_ack",
                "session_id": session_id,
                "calculated_composure": composure_index,
                "ripple_effect": "stable" if composure_index > 50 else "market_cascade_imminent"
            })
            
            await asyncio.sleep(0.01) # Maintain sub-50ms processing pipeline loops
            
    except WebSocketDisconnect:
        print(f"Session {session_id} disconnected from telemetry stream.")
    except Exception as e:
        await websocket.send_json({"event": "error", "detail": str(e)})
        await websocket.close()
