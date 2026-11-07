from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
import os

app = FastAPI(title="MRG Engine Core", version="1.0.0")

class FeedbackModel(BaseModel):
    message: str

async def run_sandbox_simulation(session=None, scenario_id: str = "default"):
    """
    Simulates real-time telemetry streaming for executive composure stress testing.
    """
    yield {"type": "scenario_start", "scenario": scenario_id}
    yield {"type": "scenario_complete", "metrics": {"composure_score": 80}, "debrief": "Done"}

@app.get("/healthz", status_code=200)
async def healthz():
    return {"status": "OK"}

@app.get("/readyz", status_code=200)
async def readyz():
    return {"ready": True}

@app.get("/api/version")
async def get_version():
    return {"version": "1.0.0"}

@app.get("/api/pricing")
async def get_pricing():
    return {"tier": "enterprise", "currency": "USD", "billing": "per_simulation_grid"}

@app.post("/api/feedback")
async def post_feedback(feedback: FeedbackModel):
    if feedback.message == "Works":
        return {"status": "accepted"}
    raise HTTPException(status_code=400, detail="Invalid Message")

@app.websocket("/ws/simulation")
async def websocket_simulation(websocket: WebSocket):
    await websocket.accept()
    try:
        async for frame in run_sandbox_simulation(scenario_id="boardroom_cyber_warfare"):
            await websocket.send_json(frame)
    finally:
        await websocket.close()
