from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mrg.core.database import init_db
from mrg.routers import webhooks
from mrg.core.billing import create_production_checkout
import os

app = FastAPI(title="MRG — Production Simulation Suite Grid")

# Initialize database connections on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Mount the live Webhook listener
app.include_router(webhooks.router)

# Live Checkout Redirect Link Generator Route
@app.post("/api/billing/checkout")
async def target_checkout_session(user_id: str, plan_tier: str, email: str = None):
    try:
        checkout_url = create_production_checkout(user_id=user_id, plan_name=plan_tier, customer_email=email)
        return {"url": checkout_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Existing basic health indicators from the repository architecture
@app.get("/healthz")
def health_check():
    return {"status": "ok", "version": "2.0.0", "mode": "production"}

@app.get("/readyz")
def readiness_check():
    return {"status": "ready"}
