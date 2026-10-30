import os
import httpx
from fastapi import HTTPException

class DeepSeekMacroClient:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.endpoint = "https://deepseek.com"

    async def calculate_systemic_ripple(self, payload_text: str, current_state: dict) -> dict:
        if not self.api_key:
            return {"status": "unauthenticated_fallback", "indices": "static_nominal"}
            
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        body = {
            "model": "deepseek-v3",
            "messages": [
                {"role": "system", "content": "You are a real-time macro-economic calculation node. Return JSON indices matching market ripple adjustments."},
                {"role": "user", "content": f"Context: {current_state}. Incident input: {payload_text}"}
            ],
            "response_format": {"type": "json_object"}
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.endpoint, headers=headers, json=body, timeout=4.0)
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(status_code=502, detail=f"Macro Engine connection failed: {e}")
