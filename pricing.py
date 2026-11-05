"""
mrg/pricing.py
Defines the official subscription tiers, capabilities, and pricing matrix.
Maps local checkout packages to Stripe Price IDs where applicable.
"""

from pydantic import BaseModel
from typing import Dict, List, Optional
import os

class PricingPlan(BaseModel):
    id: str
    name: str
    price_monthly: float
    price_yearly: Optional[float] = None
    features: List[str] = []
    stripe_price_id: Optional[str] = None
    is_self_serve: bool = True

# Subscription Core Matrix
TIERS: Dict[str, PricingPlan] = {
    "sandbox": PricingPlan(
        id="sandbox",
        name="Sandbox",
        price_monthly=0.0,
        features=["Single crisis simulation channel", "Basic offline macro engine", "Mock telemetry telemetry channels"],
        stripe_price_id=os.getenv("STRIPE_PRICE_SANDBOX", "price_mock_sandbox"),
        is_self_serve=True
    ),
    "starter": PricingPlan(
        id="starter",
        name="Starter",
        price_monthly=49.0,
        price_yearly=470.0,
        features=["Up to 3 concurrent simulations", "DeepSeek-V3 live macro connection", "Standard WebSocket telemetry stream"],
        stripe_price_id=os.getenv("STRIPE_PRICE_STARTER", "price_mock_starter"),
        is_self_serve=True
    ),
    "growth": PricingPlan(
        id="growth",
        name="Growth",
        price_monthly=499.0,
        price_yearly=4790.0,
        features=["Unlimited concurrent simulations", "Full NVIDIA Omniverse/Riva multi-sensory support", "Advanced cyber warfare & macro modules"],
        stripe_price_id=os.getenv("STRIPE_PRICE_GROWTH", "price_mock_growth"),
        is_self_serve=True
    ),
    "molecular_saas": PricingPlan(
        id="molecular_saas",
        name="Molecular SaaS",
        price_monthly=15000.0,
        price_yearly=150000.0,
        features=[
            "Generative discovery and conformer workloads for R&D teams",
            "Planet-scale crisis simulation grids",
            "Dedicated high-stakes interactive digital twins",
            "Hyper-scale workload provisioning"
        ],
        # Replace this with the actual price ID generated inside your Stripe Dashboard
        stripe_price_id=os.getenv("STRIPE_PRICE_MOLECULAR_SAAS", "price_1T37dxR9bpZJwHWs_MOLECULAR_SAAS"),
        is_self_serve=True
    ),
    "enterprise": PricingPlan(
        id="enterprise",
        name="Enterprise",
        price_monthly=0.0,
        features=["Custom deployment (On-Prem / Private VPC)", "SLA guaranteed uptimes", "Custom vertical crisis scenarios"],
        stripe_price_id=None,
        is_self_serve=False  # Requires reaching out to sales team
    )
}

def get_plan_by_id(plan_id: str) -> Optional[PricingPlan]:
    """Helper method utilized by checkout_engine.py to look up valid tiers"""
    normalized_id = plan_id.lower().replace(" ", "_")
    return TIERS.get(normalized_id)

def get_all_active_plans() -> List[PricingPlan]:
    """Returns available pricing configurations for rendering in UI views"""
    return list(TIERS.values())
