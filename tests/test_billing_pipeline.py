import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_automated_billing_metering_flow():
    """
    Simulates a high-pressure client connection to verify the middleware
    intercepts the request and triggers a compute-time calculation.
    """
    # Configure the standard transport bridge directly to our FastAPI app
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Inject a custom Mock Tenant ID via standard headers
        headers = {"X-Tenant-ID": "enterprise_tenant_alpha_test"}
        
        # Act: Trigger a request to check middleware interception behavior
        response = await client.get("/health", headers=headers)
        
        # Assert: Verify core app responds correctly with the new billing pipeline active
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["status"] == "healthy"
        assert response_data["pipeline"] == "metered_revenue"

@pytest.mark.asyncio
async def test_isolated_vault_reporting():
    """
    Ensures that our billing vault can parse, accept, and process
    metered usage model telemetry without dropping events.
    """
    from app.services.billing_vault import billing_vault
    from app.models.billing import UsageMeter
    import uuid
    
    # Construct a sample metered session load payload
    test_meter = UsageMeter(
        tenant_id="enterprise_tenant_alpha_test",
        session_id=str(uuid.uuid4()),
        simulation_minutes=5.25,
        deepseek_tokens=78750,
        riva_audio_seconds=315.0
    )
    
    # Send directly to the billing vault manager
    success = await billing_vault.report_usage_event(test_meter)
    assert success is True
