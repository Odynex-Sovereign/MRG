# tests/mock_client_test.py
import asyncio
import json
import websockets
from database.db_client import get_db_connection

async def seed_test_session():
    """Seeds an active simulation record attached to a high-margin Tier 3 Platinum license."""
    print("Seeding localized database profile with explicit subscription tier structure...")
    conn = get_db_connection()
    if not conn:
        print("Database not reached. Proceeding under default cloud sandbox fallback.")
        return
    try:
        with conn.cursor() as cur:
            # Upsert active master baseline session
            cur.execute(
                "INSERT INTO simulation_sessions (session_id, vertical) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                ("integration_test_session", "Banking & Capital Risks")
            )
            # Provision Tier 3 Master subscription credentials
            cur.execute(
                "INSERT INTO billing_subscriptions (session_id, platform_tier, pricing_architecture, billing_value, target_margin_pct) VALUES (%s, %s, %s, %s, %s)",
                ("integration_test_session", "tier_3", "monthly_master_sync", 160000.00, 92.1)
            )
        conn.commit()
        print("Successfully provisioned active Tier 3 testing subscription tier.")
    except Exception as e:
        print(f"Database already populated or skipped initialization: {e}")
    finally:
        conn.close()

async def run_smoke_test():
    await seed_test_session()
    uri = "ws://localhost:8000/ws/simulation/integration_test_session"
    print(f"Connecting smoke client engine context to channel: {uri}")
    try:
        async with websockets.connect(uri) as websocket:
            init_frame = await websocket.recv()
            print(f"[Verification Handshake Ack]: {init_frame}")
            
            mock_payload = {"vocal_stress": 0.15, "decision_velocity": 4.2}
            await websocket.send(json.dumps(mock_payload))
            
            telemetry_echo = await websocket.recv()
            print(f"[Engine Real-time Computations]: {telemetry_echo}")
    except Exception as e:
        print(f"Licensing pipeline validation failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_smoke_test())
