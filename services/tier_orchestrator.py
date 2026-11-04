import uuid
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel

logger = logging.getLogger("mrg.services.tier_orchestrator")

class UserTierDefinition(BaseModel):
    name: str
    price_label: str
    monthly_cost_usd: float
    max_visual_nodes: int
    has_out_of_band_sms: bool
    has_deepseek_reasoning: bool
    is_kid_safe: bool  # Enforces safe minimums and absolute tracking privacy

class ComprehensiveTierOrchestrator:
    """
    Manages global user permissions, youth protection gating, and 
    Figma-style sandbox sharing configurations across the 5 Fly Machines.
    """
    def __init__(self, db_client):
        self.db = db_client
        self.tiers: Dict[str, UserTierDefinition] = {
            "junior_academy": UserTierDefinition(
                name="Junior Academy Sandbox",
                price_label="Free Educational Tier",
                monthly_cost_usd=0.00,
                max_visual_nodes=15,
                has_out_of_band_sms=False,      # Redirects to internal log box for safety
                has_deepseek_reasoning=False,   # Routes through deterministic local playground
                is_kid_safe=True
            ),
            "free_community": UserTierDefinition(
                name="Community Sandbox",
                price_label="Free Regular Tier",
                monthly_cost_usd=0.00,
                max_visual_nodes=10,
                has_out_of_band_sms=False,
                has_deepseek_reasoning=False,
                is_kid_safe=False
            ),
            "pro_operator": UserTierDefinition(
                name="Professional Operator",
                price_label="Standard Commercial",
                monthly_cost_usd=29.00,
                max_visual_nodes=75,
                has_out_of_band_sms=True,
                has_deepseek_reasoning=True,
                is_kid_safe=False
            )
        }

    async def verify_action_safety(self, client_id: str) -> Dict[str, Any]:
        """Ensures complete visual compliance and safe defaults for younger users."""
        user_record = await self.db.fetchrow(
            "SELECT tier_level, parent_account_id FROM billing_vault WHERE client_id = $1", client_id
        )
        
        tier = user_record["tier_level"] if user_record else "junior_academy"
        definition = self.tiers.get(tier, self.tiers["junior_academy"])
        
        return {
            "tier": tier,
            "enforce_strict_privacy": definition.is_kid_safe,
            "allow_external_broadcast": not definition.is_kid_safe
     }
