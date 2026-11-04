# services/streaming/websocket_pipeline.py
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from config.billing_catalog import PRICING_TIERS
from database.db_client import get_db_connection

app = FastAPI(title="MRG Monetized Simulation Engine", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_tier_access(session_id: str) -> dict:
    """Queries DB to locate active software license entitlements."""
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
    
    # Enforce licensing evaluation step
    access_profile = verify_tier_access(session_id)
    tier_meta = PRICING_TIERS.get(access_profile["tier"], PRICING_TIERS["tier_1"])
    
    await websocket.send_json({
        "event": "connected",
        "session_id": session_id,
        "license_tier": access_profile["tier"],
        "operational_layer": tier_meta["layer"],
        "billing_framework": tier_meta["type"]
    })
    
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            vocal_stress = payload.get("vocal_stress", 0.0)
            decision_velocity = payload.get("decision_velocity", 1.0)
            composure_index = max(0.0, min(100.0, 100.0 - (vocal_stress * 50.0) - (decision_velocity * 2.0)))
            
            # Persist raw tracking telemetries to validated instances
            conn = get_db_connection()
            if conn:
                try:
                    with conn.cursor() as cur:
                        cur.insert = "INSERT INTO telemetry_logs (session_id, vocal_stress, decision_velocity) VALUES (%s, %s, %s)"
                        cur.execute(cur.insert, (session_id, vocal_stress, decision_velocity))
                    conn.commit()
                    conn.close()
                except Exception as db_err:
                    print(f"Telemetry log bypass: {db_err}")

            await websocket.send_json({
                "event": "telemetry_ack",
                "calculated_composure": composure_index,
                "margin_profile_protection": "active"
            })
            await asyncio.sleep(0.01)
            
    except WebSocketDisconnect:
        print(f"Session {session_id} detached safely.")
