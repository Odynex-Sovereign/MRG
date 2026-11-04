# services/billing/checkout_engine.py
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

router = APIRouter(prefix="/v1/checkout", tags=["revenue"])

# Set up Stripe token from active environment settings
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "mock_key_for_sandbox")

class CheckoutRequest(BaseModel):
    session_id: str
    tier_id: str

@router.post("/create-session")
async def create_checkout_session(payload: CheckoutRequest):
    """
    Builds an automated payment checkout link for self-serve client onboarding.
    """
    # Fallback to sandbox mode simulation if credentials are missing
    if STRIPE_SECRET_KEY == "mock_key_for_sandbox":
        mock_redirect = f"https://fly.dev"
        print(f"[SANDBOX ENGAGED] Simulating payment generation for {payload.tier_id}")
        return {"checkout_url": f"https://stripe.com_{payload.session_id}"}

    import stripe
    stripe.api_key = STRIPE_SECRET_KEY

    # Pricing maps matched back to your central 11-tier architecture matrix
    price_catalog = {
        "tier_1": {"amount": 1500000, "name": "Molecular SaaS Commercial License"},
        "tier_2": {"amount": 3500000, "name": "Infrastructure Regional Base License"},
        "tier_3": {"amount": 16000000, "name": "Platinum CAVE Master Sync"},
        "tier_5": {"amount": 8500000, "name": "Commodities Tracking Retainer"},
        "tier_7": {"amount": 11500000, "name": "Autonomous Aquatics Logistics License"},
        "tier_9": {"amount": 450000, "name": "Precision Ag Grower Software Retainer"},
    }

    tier_info = price_catalog.get(payload.tier_id)
    if not tier_info:
        raise HTTPException(status_code=400, detail="Requested tier requires a custom enterprise retainer contract.")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': tier_info["name"]},
                    'unit_amount': tier_info["amount"],  # Defined in cents
                    'recurring': {'interval': 'month'}
                },
                'quantity': 1,
            }],
            mode='subscription',
            metadata={
                'session_id': payload.session_id,
                'tier_id': payload.tier_id
            },
            success_url='https://fly.dev' + payload.session_id,
            cancel_url='https://fly.dev',
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Add this code block directly inside the price_catalog dictionary of services/billing/checkout_engine.py

    price_catalog = {
        "tier_starter": {"amount": 4900, "name": "Solo Practitioner License"},
        "tier_growth": {"amount": 49900, "name": "Emerging Team License"},
        # Keep existing high-tier mappings intact...
