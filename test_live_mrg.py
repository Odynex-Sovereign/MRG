import asyncio
import websockets
import json

async def test_simulation_stream():
    # Targeted live deployment URL
    uri = "wss://mrg.fly.dev/ws/simulation"
    
    print(f"Connecting to live MRG Crisis Simulation Gateway at {uri}...")
    async with websockets.connect(uri) as websocket:
        # Await the core engine's connection handshake response
        handshake = await websocket.recv()
        print(f"<- [System Broadcast]: {handshake}")
        
        # Craft a high-stakes scenario payload token
        payload = {
            "action": "TRIGGER_CRISIS",
            "prompt": "Global logistics pipeline freeze down due to sovereign deep-sea port grid failures."
        }
        
        print(f"-> [Client Broadcast]: Triggering crisis scenario token...")
        await websocket.send(json.dumps(payload))
        
        # Listen for real-time Macro-Cognitive ripple responses
        macro_response = await websocket.recv()
        print(f"<- [Macro-Cognitive Update]: {macro_response}")
        
        # Listen for sensory soundstream telemetry confirmation
        sensory_response = await websocket.recv()
        print(f"<- [Sensory Stream Info]: {sensory_response}")

if __name__ == "__main__":
    asyncio.run(test_simulation_stream(
    ))
