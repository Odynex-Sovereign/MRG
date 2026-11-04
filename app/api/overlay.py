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
from services.procurement_crawler import ProgrammaticProcurementCrawler

@app.on_event("startup")
async def initialize_client_acquisition():
    # Instantiate the automated B2B customer ingestion engine
    crawler = ProgrammaticProcurementCrawler(
        db_client=db_client,  # Points to your global asyncpg pool
        comms_orchestrator=social_webhook_orchestrator  # Points to your comms script
    )
    
    # Run the background tracking loop completely hands-off separate from web traffic threads
    asyncio.create_task(crawler.start_autonomous_acquisition_loop())
from app.api import marketplace as marketplace_router
from services.procurement_crawler import ProgrammaticProcurementCrawler

# 1. Register the headless API and marketplace endpoints
app.include_router(marketplace_router.router)

# 2. Boot up the autonomous client-acquisition loop at server launch
@app.on_event("startup")
async def launch_passive_income_acquisition():
    crawler = ProgrammaticProcurementCrawler(
        db_client=db_client,  # Maps to your asyncpg pool instance
        comms_orchestrator=social_webhook_orchestrator  # Maps to your social webhook instance
    )
    asyncio.create_task(crawler.start_autonomous_acquisition_loop())
    logger.info("[MRG Cluster] Version 39 autonomous procurement loops initialized.")
from services.yield_arbitrage import ComputeYieldArbitrageEngine

@app.on_event("startup")
async def initialize_high_frequency_monetization():
    # Instantiate the complete real-time yield optimizer
    yield_engine = ComputeYieldArbitrageEngine(db_client=db_client)
    
    # Launch the task loop asynchronously separate from standard web traffic threads
    asyncio.create_task(yield_engine.start_high_frequency_yield_loop())
    logger.info("[MRG Cluster] High-frequency telemetry yield loops are live.")
from services.scenarios.partnership_engine import PartnershipOrchestrationEngine

@app.on_event("startup")
async def initialize_corporate_partnerships():
    # Hook the partnership engine directly into the application context
    partnership_engine = PartnershipOrchestrationEngine(
        db_client=db_client,
        comms_orchestrator=social_webhook_orchestrator
    )
    logger.info("[MRG Cluster] Version 40 institutional partnership logic arrays initialized.")
from services.social_syndicator import AutonomousSocialSyndicator

@app.on_event("startup")
async def initialize_autonomous_marketing():
    # Instantiate the automated content generation and syndication loop
    syndicator = AutonomousSocialSyndicator(
        db_client=db_client,  # Maps to your live asyncpg database connection
        comms_orchestrator=social_webhook_orchestrator  # Maps to your active webhooks manager
    )
    
    # Fire the loop as a background task completely separate from standard web traffic threads
    asyncio.create_task(syndicator.start_autonomous_marketing_loop())
    logger.info("[MRG Cluster] Version 45 high-impact marketing syndication loops are live.")
from fastapi import FastAPI, Depends
import asyncio
import logging
from services.social_syndicator import AutonomousSocialSyndicator
from services.marketing_router import MarketingWebhookRouter

logger = logging.getLogger("mrg.app")

# Initialize your core unified framework application instance
app = FastAPI(title="MRG Autonomous Planet-Scale Grid Suite")

@app.on_event("startup")
async def launch_complete_passive_marketing_and_yield_mesh():
    """
    Fires all high-frequency automated components at server boot.
    Orchestrates the client acquisition, financial routing, and yield loops across 10 machines.
    """
    logger.info("[MRG Cluster] Initializing complete Version 45 multi-angle infrastructure mesh...")
    
    # 1. Instantiate the outbound webhook delivery channel
    marketing_router = MarketingWebhookRouter()
    
    # 2. Boot up the autonomous social syndication loop to broadcast milestones
    syndicator = AutonomousSocialSyndicator(
        db_client=db_client, # Points to your active asyncpg connection pool
        comms_orchestrator=marketing_router # Interconnects the content loop with the delivery channel
    )
    asyncio.create_task(syndicator.start_autonomous_marketing_loop())
    
    logger.info("[MRG Cluster] Version 45 assembly complete. Infrastructure hunting loops actively deployed.")
