from typing import Dict, Any
from services.scenarios.medical_specialties import MedicalSpecialtiesSimulationEngine
from services.scenarios.industrial_grids import IndustrialGridsOrchestrator

class UniversalScenarioManager:
    """Unified entrypoint to easily swap and trigger alternative industry simulations."""
    def __init__(self, db_client, comms_orchestrator, checkout_engine):
        self.medical = MedicalSpecialtiesSimulationEngine(db_client, comms_orchestrator)
        self.industrial = IndustrialGridsOrchestrator(checkout_engine, db_client)

    async def trigger_arbitrary_industry_shock(self, target_industry: str, identity_id: str) -> Dict[str, Any]:
        if target_industry == "dentistry":
            return await self.medical.execute_dentistry_supply_crisis(identity_id)
        elif target_industry == "plastic_surgery":
            return await self.medical.execute_plastic_surgery_confidentiality_breach(identity_id)
        elif target_industry == "entertainment":
            return await self.industrial.trigger_hollywood_delay_loop(identity_id)
        elif target_industry == "aviation":
            return await self.industrial.trigger_aviation_ground_stop(identity_id)
        elif target_industry == "construction":
            return await self.industrial.trigger_construction_capital_attrition(identity_id)
        else:
            raise ValueError(f"Target industry profile vector '{target_industry}' not recognized.")
