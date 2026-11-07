import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from mrg.core.config import settings
from mrg.core.database import init_db
from mrg.core.metrics import prometheus_metrics_middleware, expose_metrics_endpoint
from mrg.routers import webhooks, simulation, auth, pages, industrial, alerts

app = FastAPI(title="MRG — Planetary Crisis Simulation Operating Grid", version="2.0.0")

@app.middleware("http")
async def add_metrics_monitoring(request, call_next):
    """Enforces non-blocking execution performance vector logging for scrapers."""
    return await prometheus_metrics_middleware(request, call_next)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="mrg/static"), name="static")

@app.on_event("startup")
def on_startup():
    """Initializes primary tables and ignites low-latency background synthesis pools."""
    init_db()
    from mrg.services.mock_data import generate_continuous_validation_metrics
    asyncio.create_task(generate_continuous_validation_metrics())

@app.get("/metrics", tags=["observability"])
def metrics():
    """Exposes infrastructure status vectors natively to active Prometheus server nodes."""
    return expose_metrics_endpoint()

# Mount Unified System Routing Matrices
app.include_router(pages.router)
app.include_router(industrial.router)
app.include_router(alerts.router)
app.include_router(webhooks.router)
app.include_router(simulation.router)
app.include_router(auth.router)

@app.get("/healthz", tags=["infrastructure-health"])
def health_check():
    return {"status": "ok", "version": "2.0.0"}

@app.get("/readyz", tags=["infrastructure-health"])
def readiness_check():
    return {"status": "ready"}
