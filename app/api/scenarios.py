from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from services.scenario_manager import UniversalScenarioManager

router = APIRouter(prefix="/api/scenarios", tags=["Dynamic Scenarios"])

class ShockExecutionRequest(BaseModel):
    industry_key: str  # "dentistry", "plastic_surgery", "entertainment", "aviation", "construction"
    target_identifier: str

def get_scenario_manager() -> UniversalScenarioManager:
    from app import db_client, social_webhook_orchestrator, unified_checkout_engine
    return UniversalScenarioManager(
        db_client=db_client,
        comms_orchestrator=social_webhook_orchestrator,
        checkout_engine=unified_checkout_engine
    )

@router.post("/execute-shock")
async def execute_industry_shock(
    payload: ShockExecutionRequest,
    manager: UniversalScenarioManager = Depends(get_scenario_manager)
):
    try:
        result = await manager.trigger_arbitrary_industry_shock(
            target_industry=payload.industry_key,
            identity_id=payload.target_identifier
        )
        return {"status": "success", "execution_telemetry": result}
    except ValueError as val_err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(val_err))
