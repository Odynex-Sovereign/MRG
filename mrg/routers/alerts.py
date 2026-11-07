import os
import httpx
from fastapi import APIRouter, BackgroundTasks, HTTPException

router = APIRouter(prefix="/api/alerts", tags=["operational-alerts"])

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

def transmit_webhook_payload(message: str, severity: str):
    """Dispatches non-blocking HTTP post payloads to active developer notification rooms."""
    color_map = {"CRITICAL": 15158332, "WARNING": 15105570, "INFO": 3447003}
    
    # 1. Dispatch to Discord Channel Matrix
    if DISCORD_WEBHOOK_URL:
        payload = {
            "embeds": [{
                "title": f"SYSTEM SYSTEM OPERATIONAL SIGNAL — {severity}",
                "description": message,
                "color": color_map.get(severity, 3447003),
                "type": "rich"
            }]
        }
        try:
            httpx.post(DISCORD_WEBHOOK_URL, json=payload, timeout=2.0)
        except Exception as e:
            print(f"[Alert System] Failed passing Discord signal: {e}")

    # 2. Dispatch to Slack Channel Matrix
    if SLACK_WEBHOOK_URL:
        payload = {"text": f"*[MRG ENGINE ALERT — {severity}]* {message}"}
        try:
            httpx.post(SLACK_WEBHOOK_URL, json=payload, timeout=2.0)
        except Exception as e:
            print(f"[Alert System] Failed passing Slack signal: {e}")

@router.post("/trigger")
async def trigger_system_alert(message: str, severity: str = "INFO", background_tasks: BackgroundTasks = BackgroundTasks()):
    """API endpoint to queue structural monitoring notifications asynchronously."""
    if severity not in ["INFO", "WARNING", "CRITICAL"]:
        raise HTTPException(status_code=400, detail="Invalid severity parameter mapping assigned.")
        
    background_tasks.add_task(transmit_webhook_payload, message, severity)
    return {"status": "alert_queued"}
