from pydantic import BaseModel
from typing import Dict

class SectorSensoryProfile(BaseModel):
    sector_id: str
    haptic_mode: str       
    olfactory_profile: str  
    default_intensity: float

PREMIUM_SECTORS_REGISTRY: Dict[str, SectorSensoryProfile] = {
    "cyber_defense": SectorSensoryProfile(
        sector_id="CYBER_DEFENSE_08",
        haptic_mode="vibrational_strain",
        olfactory_profile="chemical_hazard", 
        default_intensity=0.70
    ),
    "veterinary": SectorSensoryProfile(
        sector_id="VET_MED_04",
        haptic_mode="tissue_elasticity",
        olfactory_profile="biological_voc",  
        default_intensity=0.85
    ),
    "aviation": SectorSensoryProfile(
        sector_id="AV_PROPULSION_11",
        haptic_mode="vibrational_strain",
        olfactory_profile="industrial_burn", 
        default_intensity=1.00
    ),
    "sovereign_logistics": SectorSensoryProfile(
        sector_id="SOV_LOG_12",
        haptic_mode="logistical_drag",
        olfactory_profile="chemical_hazard",
        default_intensity=0.50
    ),
    "agriculture": SectorSensoryProfile(
        sector_id="AGRI_FARM_03",
        haptic_mode="soil_resistance",
        olfactory_profile="biological_voc",
        default_intensity=0.65
    )
}
