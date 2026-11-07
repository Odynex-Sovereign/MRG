import logging
from app.models.billing import SubscriptionTier

logger = logging.getLogger("mrg_notifications")

class NotificationGateway:
    def __init__(self):
        self.gateway_name = "MRG Automated Growth Router"

    async def dispatch_seat_limit_alert(self, tier: SubscriptionTier) -> bool:
        """
        Simulates an automated email or Slack ping to the organization admin
        when team profile expansion limits are breached, offering an instant up-tier link.
        """
        upgrade_url = f"https://fly.dev{tier.tenant_id}"
        
        email_body = f"""
        Subject: Action Required: Your MRG Workspace seat capacity has been exceeded.
        
        Hello Team Admin,
        
        Your organization ({tier.tenant_id}) has reached {tier.current_seats_used} active seats out of your allowed {tier.max_seats} seats on the '{tier.tier_name}' plan.
        
        To prevent simulation lockouts for your team members, please upgrade your billing profile to the Growth Tier:
        {upgrade_url}
        
        Thank you for scaling with the MRG Simulation Suite.
        """
        
        # Log the simulated transmission to the standard pipeline terminal output
        logger.warning(f"[PLG_GROWTH_LOOP] Seat cap limit hit for {tier.tenant_id}. Sending notification...")
        print(email_body)
        return True

notification_gateway = NotificationGateway()
