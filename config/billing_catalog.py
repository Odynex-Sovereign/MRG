# config/billing_catalog.py

PRICING_TIERS = {
    "tier_1": {
        "layer": "Molecular SaaS",
        "tech_core": "Generative Discovery NIM",
        "rate": 15000.00,
        "type": "monthly_license",
        "target_margin": 96.5
    },
    "tier_2": {
        "layer": "Infrastructure",
        "tech_core": "Cassava Shear-Thickening Gels",
        "rate": 35000.00,
        "type": "monthly_regional_base",
        "target_margin": 71.4
    },
    "tier_3": {
        "layer": "Platinum CAVE",
        "tech_core": "Omniverse CloudXR Matrix",
        "rate": 160000.00,
        "type": "monthly_master_sync",
        "target_margin": 92.1
    },
    "tier_4": {
        "layer": "Genomics",
        "tech_core": "Structural Molecular Models",
        "rate": 0.00,  # Custom Retainer Basis
        "type": "custom_retainer",
        "target_margin": 94.2
    },
    "tier_5": {
        "layer": "Commodities",
        "tech_core": "Predictive Yield Telemetry",
        "rate": 85000.00,
        "type": "monthly_tracking_retainer",
        "target_margin": 88.6
    },
    "tier_6": {
        "layer": "Banking & Quant",
        "tech_core": "Composure-Arbitrage Engine",
        "rate": 0.00,  # Custom Subscription Basis
        "type": "custom_institutional_subscription",
        "target_margin": 97.1
    },
    "tier_7": {
        "layer": "Autonomous Aquatics",
        "tech_core": "Soft-Robotic Swarm Systems",
        "rate": 115000.00,
        "type": "monthly_logistics_license",
        "target_margin": 89.4
    },
    "tier_8": {
        "layer": "Hyper-Scale Compute",
        "tech_core": "Cryogenic Containment Shields",
        "rate": 0.00,  # Enterprise Contracts
        "type": "custom_hyperscaler_contract",
        "target_margin": 93.8
    },
    "tier_9": {
        "layer": "Precision Ag",
        "tech_core": "Moisture-Adaptive Hydrogels",
        "rate": 45000.00,
        "type": "monthly_grower_retainer",
        "target_margin": 84.3
    },
    "tier_10": {
        "layer": "Demolition",
        "tech_core": "Kinetic-Dampening Composites",
        "rate": 65000.00,
        "type": "per_project_material_license",
        "target_margin": 79.6
    },
    "tier_11": {
        "layer": "Safety Apparel",
        "tech_core": "Impact-Responsive Smart Textile",
        "base_hardware_min": 145.00,
        "base_hardware_max": 385.00,
        "rate": 12.00,
        "type": "per_unit_hardware_plus_monthly_sync",
        "target_margin": 81.2
    }
}
