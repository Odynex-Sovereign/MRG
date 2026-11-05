import uuid
from typing import Dict, Any, Optional
from pydantic import BaseModel
from app.config import settings  # Inheriting your existing configuration

class StrategyPackage(BaseModel):
    id: str
    name: str
    description: str
    stripe_price_id: str
    unlocked_sectors: list[str]
    max_stress_nodes: int
    has_cognitive_ai: bool

class CommercialOrchestrator:
    def __init__(self, db_client, stripe_client):
        self.db = db_client
        self.stripe = stripe_client
        
        # 1. Creative Strategy Packages & Sectors Manifest
        self.packages: Dict[str, StrategyPackage] = {
            "boardroom_cyber": StrategyPackage(
                id="pkg_boardroom_cyber",
                name="Executive Cyber Warfare Package",
                description="High-stakes corporate espionage and breach simulations.",
                stripe_price_id="price_cyber_warfare_live",
                unlocked_sectors=["MRG_GLOBAL_MACRO_01", "MRG_GEOPOL_09"],
                max_stress_nodes=50,
                has_cognitive_ai=True
            ),
            "macro_kinetic": StrategyPackage(
                id="pkg_macro_kinetic",
                name="Macroeconomic Shock & Tactical Ops Package",
                description="Simulates military supply chain failures and currency collapses.",
                stripe_price_id="price_macro_kinetic_live",
                unlocked_sectors=["MRG_MIL_06", "MRG_GLOBAL_MACRO_01", "MRG_AUTO_04"],
                max_stress_nodes=200,
                has_cognitive_ai=True
            ),
            "higher_ed_crisis": StrategyPackage(
                id="pkg_higher_ed",
                name="Institutional Composure Suite",
                description="Tailored vertical for academic board and campus infrastructure stress testing.",
                stripe_price_id="price_higher_ed_live",
                unlocked_sectors=["MRG_Higher_Ed_Vertical"],
                max_stress_nodes=25,
                has_cognitive_ai=False
            )
        }

    # 2. Live Session Metering & Token Consumption Tracking
    async def track_session_consumption(self, session_id: str, prompt_tokens: int, completion_tokens: int):
        """
        Calculates compute usage from DeepSeek-V3 and NVIDIA NIM to pass down 
        to Stripe Metered Billing for high-frequency corporate usage.
        """
        total_compute_cost = (prompt_tokens * 0.000002) + (completion_tokens * 0.000008)
        
        # Update your Postgres tracking pool via your existing db_client
        await self.db.execute(
            "UPDATE session_telemetry SET compute_accumulated = compute_accumulated + $1 WHERE id = $2",
            total_compute_cost, session_id
        )
        return total_compute_cost

    # 3. Enterprise B2B Custom Session Provisioning
    async def provision_bespoke_simulation(self, corporate_id: str, custom_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Allows consulting firms to upload custom crisis schemas for 1-on-1 guided masterclasses.
        """
        simulation_token = f"mrg_live_session_{uuid.uuid4().hex}"
        
        # Save a unique workspace twin state to the DB
        await self.db.execute(
            "INSERT INTO billing_vault (client_id, session_token, configuration, active) VALUES ($1, $2, $3, True)",
            corporate_id, simulation_token, custom_config
        )
        return {"status": "ready", "websocket_auth_endpoint": f"/ws/simulation?token={simulation_token}"}
