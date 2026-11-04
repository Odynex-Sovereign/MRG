# services/streaming/websocket_pipeline.py
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from config.billing_catalog import PRICING_TIERS
from database.db_client import get_db_connection
from services.marketing.growth_loops import ViralGrowthEngine

app = FastAPI(title="MRG Self-Marketing Planet-Scale Suite", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount our high-frequency automated revenue webhook engine directly into the application space
from services.billing.stripe_webhooks import app as stripe_webhook_router
app.mount("/billing", stripe_webhook_router)

def verify_tier_access(session_id: str) -> dict:
    conn = get_db_connection()
    if not conn:
        return {"status": "sandbox_bypass", "tier": "tier_1"}
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT platform_tier FROM billing_subscriptions WHERE session_id = %s AND is_active = TRUE",
                (session_id,)
            )
            row = cur.fetchone()
            if row:
                return {"status": "verified", "tier": row["platform_tier"]}
    except Exception as e:
        print(f"Error querying subscription state: {e}")
    finally:
        conn.close()
    return {"status": "unlicensed_fallback", "tier": "tier_1"}

@app.websocket("/ws/simulation/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    access_profile = verify_tier_access(session_id)
    tier_meta = PRICING_TIERS.get(access_profile["tier"], PRICING_TIERS["tier_1"])
    
    await websocket.send_json({
        "event": "connected",
        "session_id": session_id,
        "license_tier": access_profile["tier"],
        "operational_layer": tier_meta["layer"]
    })
    
    last_calculated_composure = 100.0
    vertical_context = "Corporate"
    
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            if payload.get("event") == "set_context":
                vertical_context = payload.get("vertical", "Corporate")
                continue
                
            vocal_stress = payload.get("vocal_stress", 0.0)
            decision_velocity = payload.get("decision_velocity", 1.0)
            
            last_calculated_composure = max(0.0, min(100.0, 100.0 - (vocal_stress * 50.0) - (decision_velocity * 2.0)))
            
            await websocket.send_json({
                "event": "telemetry_ack",
                "calculated_composure": last_calculated_composure
            })
            await asyncio.sleep(0.01)
            
    except WebSocketDisconnect:
        # VIRAL LOOP TRIGGERS INSTANTLY ON SESSION COMPLETE
        # Instead of generic tear-down, generate an immediate shareable growth card to acquire the user's peers
        growth_card = ViralGrowthEngine.generate_viral_scorecard(
            session_id=session_id, 
            composure_score=round(last_calculated_composure, 2), 
            vertical=vertical_context
        )
        print(f"Session disconnected. Auto-marketing viral package initialized for distribution:\n{json.dumps(growth_card, indent=2)}")
