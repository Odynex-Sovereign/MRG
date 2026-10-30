import asyncio
import json
import websockets

async def simulate_simulation_stream():
    """Simulates a live edge client sending high-stress biometric telemetry."""
    uri = "ws://localhost:8000/ws/simulation"
    print(f"Connecting to MRG Stream Engine at {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            # Test Scenario 1: Higher-Ed / Youth Context
            youth_packet = {
                "user_id": "usr_b9ba31c0-0f2d-4171-be1e-d4c39170e7e1",
                "session_id": "ses_5d862002-6138-4ee0-8809-b65da9a6321b",
                "vertical": "Higher-Ed",
                "vocal_pitch_variance": 24.5,
                "vocal_energy": 68.2,
                "response_latency_ms": 320,
                "user_raw_text": "I believe my research methodology stands on solid data points despite the critique."
            }
            
            print("\n[Client -> Server] Sending Higher-Ed Telemetry Matrix...")
            await websocket.send(json.dumps(youth_packet))
            response = await websocket.recv()
            print(f"[Server -> Client] Unified Sync Response:\n{json.dumps(json.loads(response), indent=2)}")

            await asyncio.sleep(1)

            # Test Scenario 2: Asset-Defense (Odynex Axis Logistics / TUTSA Layer)
            asset_packet = {
                "user_id": "usr_b9ba31c0-0f2d-4171-be1e-d4c39170e7e1",
                "session_id": "ses_5d862002-6138-4ee0-8809-b65da9a6321b",
                "vertical": "Asset-Defense",
                "vocal_pitch_variance": 12.1,
                "vocal_energy": 85.0,
                "response_latency_ms": 90,
                "user_raw_text": "The prior art established under Odynex Axis Logistics LLC completely preempts this trade secret claim."
            }
            
            print("\n[Client -> Server] Sending Odynex Corporate Asset-Defense Telemetry Matrix...")
            await websocket.send(json.dumps(asset_packet))
            response = await websocket.recv()
            print(f"[Server -> Client] Unified Sync Response:\n{json.dumps(json.loads(response), indent=2)}")

    except Exception as e:
        print(f"Connection failed or closed: {e}")

if __name__ == "__main__":
    asyncio.run(simulate_simulation_stream())
