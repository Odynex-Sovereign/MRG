"""Macro service unit tests."""

import pytest
from mrg.services.macro import generate_macro_ripple


@pytest.mark.asyncio
async def test_sandbox_macro():
    result = await generate_macro_ripple("Market shock in energy sector", {"vertical": "Auto"})
    assert "Sandbox" in result or "Simulated" in result
    assert "energy" in result.lower() or "Market" in result


@pytest.mark.asyncio
async def test_empty_prompt_sandbox():
    result = await generate_macro_ripple("", {})
    assert isinstance(result, str)
