"""
DeepSeek-V3 macro-cognitive client for systemic ripple analysis.
"""
from __future__ import annotations

import os
import logging
from typing import Any, Dict

import httpx
from fastapi import HTTPException

logger = logging.getLogger("MRG_DeepSeek")

DEFAULT_DEEPSEEK_BASE = "https://api.deepseek.com"


class DeepSeekMacroClient:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = os.getenv("DEEPSEEK_BASE_URL", DEFAULT_DEEPSEEK_BASE)
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")  # or deepseek-reasoner

    async def calculate_systemic_ripple(
        self, payload_text: str, current_state: dict
    ) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "status": "unauthenticated_fallback",
                "indices": "static_nominal",
                "message": "DEEPSEEK_API_KEY not set — sandbox mode",
            }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self.model,
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
            "temperature": 0.3,
            "max_tokens": 1024,
        }

        url = f"{self.base_url.rstrip('/')}/chat/completions"

        async with httpx.AsyncClient(timeout=4.0) as client:
            try:
                response = await client.post(url, headers=headers, json=body)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.exception("Macro engine failure")
                raise HTTPException(
                    status_code=502, detail=f"Macro Engine connection failed: {e}"
                )
