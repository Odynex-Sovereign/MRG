import os
import httpx

class LivepeerDistributor:
    def __init__(self):
        self.api_key = os.getenv("LIVEPEER_API_KEY")
        self.base_url = "https://livepeer.studio"

    async def create_decentralized_egress_channel(self, session_id: str) -> dict:
        if not self.api_key:
            return {"playbackUrl": "mock://localhost/stream.m3u8", "status": "local_loop"}

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "name": f"mrg-session-{session_id}",
            "profiles": [
                {"name": "720p", "bitrate": 2000000, "fps": 30, "width": 1280, "height": 720},
                {"name": "480p", "bitrate": 1000000, "fps": 30, "width": 854, "height": 480}
            ]
        }

        async with httpx.AsyncClient() as client:
            res = await client.post(self.base_url, headers=headers, json=payload)
            return res.json()
