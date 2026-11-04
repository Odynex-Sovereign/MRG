import httpx
from fastapi import HTTPException


class DeepSeekMacroClient:
    def __init__(self):
        import os

        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.endpoint = "https://api.deepseek.com"

    async def calculate_systemic_ripple(self, payload_text: str, current_state: dict) -> dict:
        if not self.api_key:
            return {"status": "unauthenticated_fallback", "indices": "static_nominal"}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a real-time macro-economic calculation node. "
                        "Return JSON indices matching market ripple adjustments."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Context: {current_state}. Incident input: {payload_text}",
                },
            ],
            "response_format": {"type": "json_object"},
        }

        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                response = await client.post(
                    f"{self.endpoint}/chat/completions",
                    headers=headers,
                    json=body,
                )
                response.raise_for_status()
                return response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise HTTPException(
                status_code=502,
                detail="Macro engine connection or response failed.",
            ) from exc
