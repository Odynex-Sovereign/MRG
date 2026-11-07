import os, httpx
from fastapi import APIRouter, BackgroundTasks

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

def send_alert(msg: str):
    url = os.getenv("DISCORD_WEBHOOK_URL")
    if url: httpx.post(url, json={"content": msg}, timeout=2.0)

@router.post("/trigger")
async def trigger_alert(message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_alert, message)
    return {"status": "queued"}
