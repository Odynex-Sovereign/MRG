import httpx
from api_keys import DEEPSEEK_API_KEY, IS_SANDBOX

DEEPSEEK_API_URL = "https://deepseek.com"

async def generate_macro_ripple(prompt: str) -> str:
    if IS_SANDBOX:
        return "[SANDBOX MOCK] Macro-Cognitive Layer: Simulated butterfly effect triggered globally."
        
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-v3",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
