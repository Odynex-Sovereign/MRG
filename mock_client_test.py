"""Manual / integration smoke client against a running server."""

from __future__ import annotations

import asyncio
import json
import os
import sys

try:
    import websockets
except ImportError:
    print("Install websockets: pip install websockets")
    sys.exit(1)

URI = os.getenv("MRG_WS_URL", "ws://localhost:8000/ws/simulation")


async def main() -> None:
    print(f"Connecting to {URI} ...")
    async with websockets.connect(URI) as websocket:
        status = await websocket.recv()
        print("STATUS:", status)

        packet = {
            "user_id": "usr_smoke",
            "session_id": "ses_smoke",
            "vertical": "Higher-Ed",
            "vocal_pitch_variance": 24.5,
            "vocal_energy": 68.2,
            "response_latency_ms": 320,
            "user_raw_text": "I believe my research methodology stands on solid data.",
        }
        await websocket.send(json.dumps(packet))
        print("RECV:", await websocket.recv())
        print("RECV:", await websocket.recv())

        await websocket.send(
            json.dumps({"action": "TRIGGER_CRISIS", "prompt": "Sudden energy supply disruption"})
        )
        print("RECV:", await websocket.recv())
        print("RECV:", await websocket.recv())


if __name__ == "__main__":
    asyncio.run(main())
