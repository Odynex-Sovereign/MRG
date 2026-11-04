FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 1. Create a clean requirements layer right inside the build engine
RUN echo "fastapi>=0.100.0\nuvicorn[standard]>=0.22.0\npydantic>=2.0.0\nhttpx>=0.24.0" > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 2. Inject a completely fresh, self-contained multi-sensory application script 
# This completely replaces the need to edit separate websocket files on your phone screen
RUN mkdir -p services/streaming && echo ' \n\
import asyncio \n\
from fastapi import FastAPI, WebSocket, WebSocketDisconnect \n\
from pydantic import BaseModel \n\
from typing import Dict \n\
app = FastAPI(title="MRG Crisis Simulation Grid") \n\
class SensoryPacket(BaseModel): \n\
    haptic_frequency: float \n\
    haptic_intensity: float \n\
    scent_profile_id: str \n\
    concentration_ppm: float \n\
@app.get("/") \n\
async def root(): \n\
    return {"status": "healthy", "service": "MRG Premium Engine Stack"} \n\
@app.websocket("/ws/simulation/{session_id}") \n\
async def simulation(websocket: WebSocket, session_id: str, user_tier: str = "Standard"): \n\
    await websocket.accept() \n\
    try: \n\
        while True: \n\
            data = await websocket.receive_json() \n\
            if data.get("action") == "trigger_crisis_event": \n\
                await websocket.send_json({"event": "SENSORY_TELEMETRY", "data": {"haptic_frequency": 145.5, "haptic_intensity": 0.85, "scent_profile_id": data.get("scent_trigger", "NONE"), "concentration_ppm": 12.5}}) \n\
    except WebSocketDisconnect: \n\
        pass \n\
' > services/streaming/websocket_pipeline.py

# 3. Mount all secondary environment configurations
COPY . .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 4. Initialize the web process loop bound to the open network interface adapter
CMD ["python", "-m", "uvicorn", "services.streaming.websocket_pipeline:app", "--host", "0.0.0.0", "--port", "8000"]
