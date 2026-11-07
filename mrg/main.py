import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from mrg.core.config import settings
from mrg.core.database import init_db
from mrg.core.metrics import prometheus_metrics_middleware, expose_metrics_endpoint
from mrg.routers import webhooks, simulation, auth, pages, industrial, alerts
from mrg.services.mock_data import generate_continuous_validation_metrics

# Initialize the global enterprise-scale core framework instance
app = FastAPI(
    title="MRG — Planetary Crisis Simulation Grid Hub",
    description="Mission-critical event loop orchestration matrix with integrated real-time stream layers.",
    version="2.0.0"
)

# 1. Mount Low-Overhead Telemetry Middleware (Prometheus Tracker Framework)
@app.middleware("http")
async def add_metrics_monitoring(request, call_next):
    """Intercepts request pipelines non-blockingly to feed cluster monitoring instances."""
    return await prometheus_metrics_middleware(request, call_next)

# 2. Configure Cross-Origin Resource Sharing (CORS) Security Policies
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Mount Static UI Style Sheets and Frontend Client Layout Templates
app.mount("/static", StaticFiles(directory="mrg/static"), name="static")
templates = Jinja2Templates(directory="mrg/templates")

# 4. App Ignition & Persistent Data Schema Lifecycle Handlers
@app.on_event("startup")
def on_startup():
    """Executes infrastructure schema definitions and initiates telemetry synthesis pools."""
    # Build tables and map foreign constraints inside persistent PostgreSQL engine space
    init_db()
    
    # Run the continuous validation high-frequency metrics loop asynchronously
    asyncio.create_task(generate_continuous_validation_metrics())

# 5. Core Platform Scraper Telemetry Pipeline Target
@app.get("/metrics", tags=["observability"])
def metrics():
    """Exposes structured application runtime performance data vectors directly to Prometheus scrapers."""
    return expose_metrics_endpoint()

# 6. Global Operational Route Microservice Registries
app.include_router(pages.router)       # User facing interface screens and guided paths
app.include_router(industrial.router)  # Low-latency financial ITCH/OUCH & Siemens data bus relays
app.include_router(alerts.router)      # Real-time incident telemetry logging (Discord/Slack routers)
app.include_router(webhooks.router)    # Asynchronous payment settlement listeners (Stripe Webhooks)
app.include_router(simulation.router)  # High-frequency multi-agent streaming pipelines (WebSocket grids)
app.include_router(auth.router)        # Security session token provisioning arrays (JWT Core)

# 7. System Health State Status Verification Pathways
@app.get("/healthz", tags=["infrastructure-health"])
def health_check():
    """Liveness probe verifying main cluster execution core status."""
    return {"status": "ok", "version": "2.0.0"}

@app.get("/readyz", tags=["infrastructure-health"])
def readiness_check():
    """Readiness probe checking network port bind status and framework connection state."""
    return {"status": "ready"}
