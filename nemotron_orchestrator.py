"""
NVIDIA Nemotron-4 / NIM micro-tactical orchestrator.
Uses OpenAI-compatible NVIDIA NIM endpoints for sub-50ms conversational loops.
"""
from __future__ import annotations

import os
import logging
from typing import List, Dict, Any

import httpx
from fastapi import HTTPException

logger = logging.getLogger("MRG_Nemotron")

# Official NVIDIA NIM OpenAI-compatible base (adjust to your deployed NIM)
DEFAULT_NIM_BASE = "https://integrate.api.nvidia.com/v1"


class NemotronOrchestrator:
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_NIM_API_KEY")
        self.base_url = os.getenv("NVIDIA_NIM_BASE_URL", DEFAULT_NIM_BASE)
        self.model = os.getenv("NVIDIA_NIM_MODEL", "nvidia/nemotron-4-340b-instruct")

    async def generate_adversarial_turn(
        self, prompt_id: str, context_history: List[Dict[str, str]]
    ) -> str:
        """
        Generate the next adversarial / coaching turn for the crisis simulation.
        Falls back to sandbox mode when no API key is present.
        """
        if not self.api_key:
            return (
                "[SANDBOX_MODE] Micro-tactical loop operational. "
                "Live NVIDIA NIM key missing. Inject NVIDIA_NIM_API_KEY for production."
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": context_history,
            "temperature": 0.2,
            "max_tokens": 150,
            "stream": False,
        }

        url = f"{self.base_url.rstrip('/')}/chat/completions"

        async with httpx.AsyncClient(timeout=1.5) as client:
            try:
                res = await client.post(url, headers=headers, json=payload)
                res.raise_for_status()
                data = res.json()
                return data["choices"][0]["message"]["content"]
            except httpx.TimeoutException:
                raise HTTPException(
                    status_code=504, detail="Micro-tactical NIM timeout (>1.5s)"
                )
            except Exception as e:
                logger.exception("Nemotron call failed")
                raise HTTPException(
                    status_code=502, detail=f"Micro tactical engine error: {e}"
                )
