from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any
from services.tier_orchestrator import ComprehensiveTierOrchestrator

# Ensure your global FastAPI app instance exists
app = FastAPI(title="MRG Integrated Simulation Grid Engine")

# Dependency injector to bind your database pool to the Tier Orchestrator
def get_tier_orchestrator() -> ComprehensiveTierOrchestrator:
    from app import db_client # Points to your global asyncpg database client object
    return ComprehensiveTierOrchestrator(db_client=db_client)

class DeployGridRequest(BaseModel):
    client_id: str
    node_count: int

@app.post("/api/tiers/verify-deploy")
async def verify_grid_deployment(
    request: DeployGridRequest, 
    orchestrator: ComprehensiveTierOrchestrator = Depends(get_tier_orchestrator)
):
    """
    Enforces subscription gates before spawning new simulation nodes.
    Protects compute resources across your 5 Fly Machines.
    """
    # 1. Verify user profile and safety configurations
    safety_profile = await orchestrator.verify_action_safety(request.client_id)
    
    # 2. Gate execution boundaries based on visual limitations matrix
    tier_key = safety_profile["tier"]
    allowed_nodes = orchestrator.tiers[tier_key].max_visual_nodes
    
    if request.node_count > allowed_nodes:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Deployment capped. {tier_key.upper()} profiles are limited to {allowed_nodes} active visual nodes."
        )
        
    return {
        "status": "authorized",
        "enforce_strict_privacy": safety_profile["enforce_strict_privacy"],
        "max_capacity": allowed_nodes
 }
