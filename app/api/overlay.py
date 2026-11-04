from fastapi import APIRouter, Depends
from typing import Dict, Any
from services.virtual_overlay import VirtualDataFederationOverlay

router = APIRouter(prefix="/api/overlay", tags=["Data Federation"])

# Placeholder function to re-use your existing database client object safely
def get_db_client():
    from app import db_client # Adjust mapping context to point to your main module instance
    return db_client

@router.get("/metrics-stream", response_model=Dict[str, Any])
async def get_metrics_stream(db = Depends(get_db_client)):
    """Fetches a real-time, non-persisted federation frame to update client charts."""
    orchestrator = VirtualDataFederationOverlay(db_client=db)
    return await orchestrator.generate_federated_analytics_map()
from app.api import scenarios as scenario_router

# Include your expanded dynamic scenarios router schema alongside existing layers
app.include_router(scenario_router.router)
from services.scenarios.hyper_scale import HyperScaleOrchestrationEngine

@app.on_event("startup")
async def schedule_hyperscale_tasks():
    # Instantiate the complete parallel infrastructure engine
    fleet_engine = HyperScaleOrchestrationEngine(
        db_client=db_client,  # Maps to your active global asyncpg database client object
        comms_orchestrator=social_webhook_orchestrator  # Maps to your comms variable
    )
    
    # Run the background tracking loop asynchronously inside the app process thread pool
    asyncio.create_task(fleet_engine.launch_autonomous_fleet_recovery_monitor())
