import os
import httpx
from typing import Dict, Any

class DeepSeekOrchestrator:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.endpoint = "https://deepseek.com" 

    async def generate_crisis_step(self, sector: str, current_state: str) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "cascade_summary": "[SANDBOX MODE] API Key missing. Systemic degradation simulated.",
                "sensory_telemetry": {
                    "haptic_frequency": 45.0, 
                    "haptic_intensity": 0.3,
                    "scent_profile_id": "SANDBOX_DEFAULT_00", 
                    "concentration_ppm": 1.0
                }
            }

        system_prompt = (
            "You are the Macro-Cognitive Tier of the MRG Crisis Grid.\n"
            "You evaluate systemic ripple effects across macroeconomics, industry, and biology.\n"
            "CRITICAL: You must include a structured 'sensory_telemetry' JSON block mapping the physical reality.\n"
            "Map physical breakdown to frequency/intensity vectors, and biochemical or ambient states "
            "to specific alphanumeric scent IDs derived from the system manifest."
        )

        user_content = f"Sector: {sector}. Current Emergency Vector: {current_state}."

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.endpoint}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}", 
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ],
                    "response_format": {"type": "json_object"},
                    "temperature": 0.3
                },
                timeout=30.0
            )
            return response.json()
