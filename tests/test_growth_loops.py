import pytest
from app.models.billing import SubscriptionTier
from app.services.notification_gateway import notification_gateway
from app.services.billing_vault import billing_vault

@pytest.mark.asyncio
async def test_seat_limit_breach_detection():
    """
    Verifies that adding a member beyond tier thresholds correctly logs 
    a limit breach and triggers the expansion payload.
    """
    # Create a mock customer tier that is currently breaking its allocation matrix
    over_capacity_tier = SubscriptionTier(
        tenant_id="alpha_corp_labs",
        tier_name="Developer",
        max_seats=5,
        current_seats_used=6
    )
    
    # 1. Enforce checks via our billing vault validator logic
    allowed = await billing_vault.enforce_seat_limits(
        tenant_id=over_capacity_tier.tenant_id,
        requested_seats=over_capacity_tier.current_seats_used,
        max_seats=over_capacity_tier.max_seats
    )
    assert allowed is False  # System must flag this as over-capacity
    
    # 2. Dispatch automated expansion notification
    sent = await notification_gateway.dispatch_seat_limit_alert(over_capacity_tier)
    assert sent is True
