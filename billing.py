"""
Stripe billing integration for MRG subscription tiers.
"""
from __future__ import annotations

import os
import logging
from typing import Optional

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel

logger = logging.getLogger("MRG_Billing")

router = APIRouter(prefix="/api/billing", tags=["Billing & Monetization"])

try:
    import stripe
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
except ImportError:
    stripe = None  # type: ignore

ENDPOINT_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")


class CheckoutSessionRequest(BaseModel):
    user_id: str
    price_id: str


@router.post("/create-checkout-session")
async def create_checkout_session(req: CheckoutSessionRequest):
    """Generates a secure checkout link for monetization tiers."""
    if not stripe or not stripe.api_key:
        return {
            "checkout_url": f"https://mrg-simulation-grid.fly.dev/pricing?sandbox=1&user={req.user_id}",
            "mode": "sandbox",
            "message": "STRIPE_SECRET_KEY not configured — returning mock URL",
        }

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": req.price_id, "quantity": 1}],
            mode="subscription" if "sub" in req.price_id else "payment",
            success_url="https://mrg-simulation-grid.fly.dev/dashboard?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://mrg-simulation-grid.fly.dev/pricing",
            client_reference_id=req.user_id,
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stripe error: {e}")


@router.post("/webhook")
async def stripe_webhook(
    request: Request, stripe_signature: Optional[str] = Header(None)
):
    """Handles Stripe webhook events for subscription lifecycle."""
    if not stripe or not ENDPOINT_SECRET:
        return {"status": "ignored", "reason": "stripe_not_configured"}

    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, ENDPOINT_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid signature: {e}")

    event_type = event["type"]
    session = event["data"]["object"]
    user_id = session.get("client_reference_id")

    if event_type == "checkout.session.completed":
        logger.info("[BILLING] Activation verified for user: %s", user_id)
    elif event_type in ("customer.subscription.deleted", "invoice.payment_failed"):
        logger.info("[BILLING] Deactivation verified for user: %s", user_id)

    return {"status": "success"}
