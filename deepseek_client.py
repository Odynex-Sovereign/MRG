# services/cognitive/deepseek_client.py
import os
import httpx
from typing import Dict, Any

class DeepSeekMacroClient:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY", "sandbox_key")
        self.base_url = "https://deepseek.com" # OpenAI-compatible endpoint
        
    async def analyze_systemic_ripple(self, vertical: str, context_state: Dict[str, Any]) -> Dict[str, Any]:
        if self.api_key == "sandbox_key":
            # Graceful sandbox mode fallback
            return {
                "mode": "sandbox",
                "macro_cascade": "Sandbox simulation triggered. No deep systemic effects generated.",
                "severity_index": 0.1
            }
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"Analyze structural ripple effects for the {vertical} vertical given this data state: {json.dumps(context_state)}"
        
        payload = {
            "model": "deepseek-chat", # DeepSeek-V3 chat identifier
            "messages": [
                {"role": "system", "content": "You are the macro-cognitive matrix coordinator for a planet-scale crisis grid."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, headers=headers, json=payload, timeout=30.0)
            if response.status_code == 200:
                result = response.json()
                return {
                    "mode": "production",
                    "macro_cascade": result["choices"][0]["message"]["content"],
                    "severity_index": 0.85
                }
            else:
                raise Exception(f"DeepSeek client failure: {response.status_code} - {response.text}")
