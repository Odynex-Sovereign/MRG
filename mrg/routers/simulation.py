from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from mrg.services.simulation import stream_manager

router = APIRouter(prefix="/api/simulation", tags=["simulation"])

@router.websocket("/stream")
async def simulation_telemetry_stream(websocket: WebSocket):
    await stream_manager.connect(websocket)
    try:
        await stream_manager.broadcast_telemetry(websocket)
    except WebSocketDisconnect:
        stream_manager.disconnect(websocket)
