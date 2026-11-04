"""Sensory synthesis (Riva TTS / Audio2Face) with sandbox fallback."""

from __future__ import annotations

import logging

from mrg.config import get_settings

logger = logging.getLogger("mrg.sensory")


async def synthesize_speech_stream(text: str) -> bytes:
    """Return audio bytes for the given text.

    Production integrations (NVIDIA Riva, Audio2Face) are optional. Without
    credentials the function returns a small mock payload so WebSocket clients
    still receive SENSORY_STREAM_INFO frames.
    """
    settings = get_settings()
    if not settings.enable_sensory:
        return b""

    if not settings.has_nvidia:
        # Deterministic mock so tests can assert non-zero length
        return b"MOCK_WAV_AUDIO_STREAM_DATA"

    # Placeholder for real Riva / NIM integration.
    # External gRPC or HTTP clients can be wired here without changing the API.
    logger.debug("nvidia_sensory_stub text_len=%d", len(text))
    return b"MOCK_WAV_AUDIO_STREAM_DATA"
