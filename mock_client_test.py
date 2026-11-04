# tests/mock_client_test.py
import asyncio
import websockets
import json

async def run_smoke_test():
    uri = "ws://localhost:8000/ws/simulation/test_session_01"
    print(f"Opening connection to local stream engine: {uri}")
    try:
        async with websockets.connect(uri) as websocket:
            # Read initialization acknowledgement
            welcome = await websocket.recv()
            print(f"[Engine Response]: {welcome}")
            
            # Send sample telemetry data metrics frame
            mock_telemetry = {
                "vocal_stress": 0.42,
                "decision_velocity": 12.5
            }
            print(f"[Client Sending]: {json.dumps(mock_telemetry)}")
            await websocket.send(json.dumps(mock_telemetry))
            
            # Receive real-time digital twin twin balance computation update
            ack_response = await websocket.recv()
            print(f"[Engine Calculations Echo]: {ack_response}")
            
    except Exception as e:
        print(f"Pipeline connectivity test failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_smoke_test())
