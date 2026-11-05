import logging
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import stripe
from app.config import settings

router = APIRouter(prefix="/api/checkout", tags=["Stripe Checkout Matrix"])

class SessionRequestPayload(BaseModel):
    price_id: str
    client_id: str

@router.post("/create-session")
async def create_secure_stripe_checkout(payload: SessionRequestPayload):
    stripe_key = getattr(settings, "STRIPE_SECRET_KEY", None)
    if not stripe_key:
        logger.error("[Stripe Core] Global STRIPE_SECRET_KEY secret is unconfigured.")
        raise HTTPException(status_code=500, detail="Backend payment gate uninitialized.")
        
    stripe.api_key = stripe_key

    try:
        # MAP PRICE IDENTIFIER TO ANONYMOUS VALUE FALLBACKS IF PRODUCT KEYS LACK HARD SYNCS
        target_amount_cents = 1500000  # Default Molecular SaaS ($15,000.00 USD)
        if "base" in payload.price_id.lower() or "infrastructure" in payload.price_id.lower():
            target_amount_cents = 3500000  # Infrastructure Base ($35,000.00 USD)
        elif "cave" in payload.price_id.lower() or "master" in payload.price_id.lower():
            target_amount_cents = 16000000  # Platinum CAVE ($160,000.00 USD)

        # BUILD ADAPTIVE CHECKOUT LAYER ON THE FLY
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"MRG Institutional Allocation Tier: {payload.price_id.upper()}",
                        "description": "Planet-Scale Grid Crisis Simulation & Out-of-Band Resilience Gateway Node.",
                    },
                    "unit_amount": target_amount_cents,
                    "recurring": {"interval": "month"},
                },
                "quantity": 1,
            }],
            mode="subscription",
            success_url="https://fly.dev{CHECKOUT_SESSION_ID}",
            cancel_url="https://fly.dev",
            client_reference_id=payload.client_id,
        )
        return {"id": session.id}
        
    except Exception as e:
        logging.error(f"[Stripe Handshake Error] Failed to generate billing intent: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Stripe initialization token mismatch: {str(e)}"
     )
