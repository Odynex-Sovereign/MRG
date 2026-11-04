# services/sensory/multisensory_bridge.py
from pydantic import BaseModel
from typing import Dict, Optional

class HapticFeedback(BaseModel):
    frequency_hz: float
    intensity: float  # 0.0 to 1.0
    pattern_type: str  # "fluid_drag", "impact", "friction"
    spatial_vector: list[float]  # X, Y, Z vector of the force

class OlfactoryFeedback(BaseModel):
    scent_molecule_id: str  # e.g., "METALLIC_HEME_01", "ACETONE_KETONE_03"
    concentration: float  # Parts per million simulation metric
    duration_ms: int

class PremiumSensoryPayload(BaseModel):
    session_id: str
    user_tier: str = "Premium_Research"
    haptics: Optional[HapticFeedback] = None
    olfactory: Optional[OlfactoryFeedback] = None

class MultisensoryOrchestrator:
    """
    Blends DeepSeek-V3 physics outcomes with real-time sensory hardware instructions
    """
    def __init__(self, baseline_viscosity: float = 1.0):
        self.baseline_viscosity = baseline_viscosity

    async def calculate_vessel_feedback(self, velocity: float, proximity_to_wall: float, pathogen_detected: bool) -> PremiumSensoryPayload:
        # Calculate tactile drag inside the blood vessel
        drag_intensity = min(velocity * 0.15, 1.0)
        
        haptic_data = HapticFeedback(
            frequency_hz=120.0 if proximity_to_wall < 0.1 else 25.0,
            intensity=1.0 if proximity_to_wall == 0.0 else drag_intensity,
            pattern_type="impact" if proximity_to_wall == 0.0 else "fluid_drag",
            spatial_vector=[0.0, 0.0, -velocity]
        )
        
        # Trigger olfactory response if passing a specific biochemical anomaly
        olfactory_data = None
        if pathogen_detected:
            olfactory_data = OlfactoryFeedback(
                scent_molecule_id="BIO_NECROSIS_42",
                concentration=0.85,
                duration_ms=1200
            )
            
        return PremiumSensoryPayload(
            session_id="research_sim_alpha",
            haptics=haptic_data,
            olfactory=olfactory_data
        )
# config/premium_sectors_manifest.py
from pydantic import BaseModel
from typing import Dict, Any

class SectorSensoryProfile(BaseModel):
    sector_id: str
    haptic_mode: str       # "vibrational_strain", "tissue_elasticity", "logistical_drag"
    olfactory_profile: str  # "chemical_hazard", "biological_voc", "industrial_burn"
    default_intensity: float

PREMIUM_SECTORS_REGISTRY: Dict[str, SectorSensoryProfile] = {
    "cyber_defense": SectorSensoryProfile(
        sector_id="CYBER_DEFENSE_08",
        haptic_mode="vibrational_strain",
        olfactory_profile="chemical_hazard", # Ozone/Electrical arcing
        default_intensity=0.70
    ),
    "veterinary": SectorSensoryProfile(
        sector_id="VET_MED_04",
        haptic_mode="tissue_elasticity",
        olfactory_profile="biological_voc",  # Pathogen/Necrosis analogs
        default_intensity=0.85
    ),
    "aviation": SectorSensoryProfile(
        sector_id="AV_PROPULSION_11",
        haptic_mode="vibrational_strain",
        olfactory_profile="industrial_burn", # Jet-A fuel/Hydraulic fluid
        default_intensity=1.00
    ),
    "sovereign_logistics": SectorSensoryProfile(
        sector_id="SOV_LOG_12",
        haptic_mode="logistical_drag",
        olfactory_profile="chemical_hazard",
        default_intensity=0.50
    )
}
