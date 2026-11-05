"""
app.py / routes.py
Standard application entrypoint ensuring safety mock endpoints function 
correctly when a live Stripe environment configuration is missing.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import os

app = FastAPI(title="MRG Grid Control")

class CheckoutRequest(BaseModel):
    plan_id: str

@app.post("/api/checkout")
async def start_checkout(payload: CheckoutRequest):
    # Retrieve configuration state
    stripe_key = os.getenv("STRIPE_SECRET_KEY")
    
    # Normalizing plan string to handle 'Molecular SaaS' or 'molecular_saas'
    plan_name = payload.plan_id.lower().replace(" ", "_")
    
    # Explicitly catch and register the new plan to prevent 404 errors
    valid_plans = ["sandbox", "starter", "growth", "molecular_saas", "enterprise"]
    if plan_name not in valid_plans:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Requested operational footprint package not found."
        )
        
    # If the system is running in sandbox mode (Missing Stripe Secrets)
    if not stripe_key:
        return {
            "status": "sandbox_success",
            "message": "System running in sandbox mode. Stripe is unconfigured.",
            "redirect_url": "/demo",
            "plan_provisioned": payload.plan_id
        }
        
    # Live production fallback routing
    return {
        "status": "live_redirect",
        "redirect_url": f"https://stripe.com{plan_name}"
 }
