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
    can_publicly_share: bool

class TierOrchestrator:
    """
    Manages multi-tier business logic, feature gating, and public deep-link 
    generation to democratize access across all financial backgrounds.
    """
    def __init__(self, db_client):
        self.db = db_client
        
        # 1. Product Matrix for Varied Financial Backgrounds
        self.tiers: Dict[str, UserTierDefinition] = {
            "free_community": UserTierDefinition(
                name="Community Sandbox",
                price_label="Free Forever",
                monthly_cost_usd=0.00,
                max_visual_nodes=10,
                has_out_of_band_sms=False,
                has_deepseek_reasoning=False, # Uses local sandbox fallback models
                can_publicly_share=True       # Viral loop mechanic
            ),
            "pro_operator": UserTierDefinition(
                name="Professional Operator",
                price_label="Standard Premium",
                monthly_cost_usd=29.00,
                max_visual_nodes=50,
                has_out_of_band_sms=True,
                has_deepseek_reasoning=True,  # Unlocks DeepSeek-V3 pipelines
                can_publicly_share=True
            ),
            "enterprise_elite": UserTierDefinition(
                name="Enterprise Command Suite",
                price_label="Corporate Training",
                monthly_cost_usd=499.00,
                max_visual_nodes=500,
                has_out_of_band_sms=True,
                has_deepseek_reasoning=True,
                can_publicly_share=True
            )
        }

    async def validate_node_deployment(self, client_id: str, requested_nodes_count: int) -> bool:
        """Enforces limits on visual nodes based on the user's active billing profile tier."""
        tier_key = await self.db.fetchval(
            "SELECT tier_level FROM billing_vault WHERE client_id = $1", client_id
        ) or "free_community"
        
        allowed_nodes = self.tiers[tier_key].max_visual_nodes
        if requested_nodes_count > allowed_nodes:
            logger.warning(f"[Tier Gate] Client {client_id} blocked: Requested {requested_nodes_count} nodes on {tier_key} tier.")
            return False
        return True

    async def generate_public_share_link(self, author_id: str, simulation_state_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Figma/Canva Playbook: Generates a fast, read-only snapshot route 
        allowing regular users to post viral creations across public channels.
        """
        share_id = f"s_{uuid.uuid4().hex[:12]}"
        
        # Save structural snapshot state to your Postgres data pool
        await self.db.execute(
            "INSERT INTO growth_loops (id, referrer_id, conversion_value, payout_settled) "
            "VALUES ($1, $2, 0, False)", share_id, author_id
        )
        
        # Return read-only mapping context endpoint for browser consumers
        return {
            "status": "published",
            "share_url": f"https://fly.dev{share_id}",
            "embed_code": f"<iframe src='https://fly.dev{share_id}' width='100%' height='500'></iframe>"
    }
