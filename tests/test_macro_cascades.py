import pytest
from services.macro_engine.deepseek_client import DeepSeekMacroClient

@pytest.mark.asyncio
async def test_fallback_macro_response_without_keys():
    client = DeepSeekMacroClient()
    # Enforces handling defaults gracefully when secrets are absent
    res = await client.calculate_systemic_ripple(
        "Canal disruption event verified", 
        {"brent_crude_price_usd": 84.50}
    )
    assert "status" in res
    assert res["indices"] == "static_nominal"
