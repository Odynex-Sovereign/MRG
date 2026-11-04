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
