import httpx
from api_keys import NVIDIA_NIM_API_KEY, IS_SANDBOX

RIVA_URI = "https://nvidia.com"

async def synthesize_speech_stream(text: str) -> bytes:
    if IS_SANDBOX:
        return b"MOCK_WAV_AUDIO_STREAM_DATA"
        
    headers = {
        "Authorization": f"Bearer {NVIDIA_NIM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": text,
        "voice": "English-US.Female-1",
        "encoding": "WAV"
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(RIVA_URI, json=payload, headers=headers)
        response.raise_for_status()
        return response.content
