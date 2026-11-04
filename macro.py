"""Macro-cognitive ripple generation (DeepSeek or sandbox fallback)."""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

from mrg.config import get_settings

logger = logging.getLogger("mrg.macro")


async def generate_macro_ripple(
    prompt: str,
    context: dict[str, Any] | None = None,
) -> str:
    """Produce systemic macro analysis for a crisis prompt.

    Returns a string analysis. In sandbox mode (no API key) returns a
    deterministic simulated response so the pipeline remains testable.
    """
    settings = get_settings()
    context = context or {}

    if not settings.has_deepseek:
        vertical = context.get("vertical") or "general"
        return (
            f"[Sandbox mode] Simulated systemic macro effects for vertical={vertical}: "
            f"{prompt[:200]}"
        )

    headers = {
        "Authorization": f"Bearer {settings.deepseek_api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": settings.deepseek_model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a real-time macro-economic and geopolitical calculation node "
                    "for crisis simulation. Return concise structured analysis of systemic "
                    "ripple effects. Prefer JSON when possible."
                ),
            },
            {
                "role": "user",
                "content": f"Context: {json.dumps(context, default=str)}. Incident: {prompt}",
            },
        ],
        "max_tokens": 1024,
        "temperature": 0.3,
    }

    try:
        async with httpx.AsyncClient(timeout=settings.deepseek_timeout_seconds) as client:
            resp = await client.post(
                f"{settings.deepseek_base_url.rstrip('/')}/v1/chat/completions",
                headers=headers,
                json=body,
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return content if isinstance(content, str) else json.dumps(content)
    except httpx.TimeoutException:
        logger.warning("deepseek_timeout")
        return f"[Timeout fallback] Macro analysis deferred for: {prompt[:120]}"
    except Exception:
        logger.exception("deepseek_request_failed")
        return f"[Error fallback] Unable to compute macro ripple for: {prompt[:120]}"
