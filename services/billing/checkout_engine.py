import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/v1/checkout", tags=["revenue"])

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "mock_key_for_sandbox")


class CheckoutRequest(BaseModel):
    session_id: str
    tier_id: str


@router.post("/create-session")
async def create_checkout_session(payload: CheckoutRequest):
    """Build a checkout link for an MRG subscription tier."""
    if STRIPE_SECRET_KEY == "mock_key_for_sandbox":
        return {
            "checkout_url": f"https://stripe.com_{payload.session_id}",
            "mode": "sandbox",
            "message": "Sandbox mode: Stripe key not configured",
        }

    import stripe

    stripe.api_key = STRIPE_SECRET_KEY
    price_catalog = {
        "tier_1": {"amount": 1500000, "name": "Molecular SaaS Commercial License"},
        "tier_2": {"amount": 3500000, "name": "Infrastructure Regional Base License"},
        "tier_3": {"amount": 16000000, "name": "Platinum CAVE Master Sync"},
        "tier_5": {"amount": 8500000, "name": "Commodities Tracking Retainer"},
        "tier_7": {"amount": 11500000, "name": "Autonomous Aquatics Logistics License"},
        "tier_9": {"amount": 450000, "name": "Precision Ag Grower Software Retainer"},
        "tier_starter": {"amount": 4900, "name": "Solo Practitioner License"},
        "tier_growth": {"amount": 49900, "name": "Emerging Team License"},
    }

    tier_info = price_catalog.get(payload.tier_id)
    if not tier_info:
        raise HTTPException(
            status_code=400,
            detail="Requested tier requires a custom enterprise retainer contract.",
        )

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": tier_info["name"]},
                    "unit_amount": tier_info["amount"],
                    "recurring": {"interval": "month"},
                },
                "quantity": 1,
            }],
            mode="subscription",
            metadata={"session_id": payload.session_id, "tier_id": payload.tier_id},
            success_url="https://fly.dev/" + payload.session_id,
            cancel_url="https://fly.dev",
        )
        return {"checkout_url": session.url}
    except Exception as exc:  # pragma: no cover - external Stripe integration
        raise HTTPException(status_code=500, detail=str(exc)) from exc
