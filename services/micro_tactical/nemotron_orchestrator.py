import os
import httpx
from fastapi import HTTPException

class NemotronOrchestrator:
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_NIM_API_KEY")
        self.url = "https://nvidia.com"

    async def generate_adversarial_turn(self, prompt_id: str, context_history: list) -> str:
        if not self.api_key:
            return "[SANDBOX_MODE] Micro-tactical loop operational. Live NVIDIA NIM key missing."

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "nvidia/nemotron-4-340b-instruct",
            "messages": context_history,
            "temperature": 0.2,
            "max_tokens": 150
        }

        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(self.url, headers=headers, json=payload, timeout=1.5)
                data = res.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                raise HTTPException(status_code=504, detail=f"Micro tactical timeout or down: {e}")
