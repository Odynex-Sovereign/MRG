import os
from typing import Optional

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel

router = APIRouter(prefix="/api/billing", tags=["Billing & Monetization"])

try:
    import stripe
except ImportError:  # Keep sandbox/startup usable without the optional billing SDK.
    stripe = None  # type: ignore[assignment]

ENDPOINT_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")


class CheckoutSessionRequest(BaseModel):
    user_id: str
    price_id: str


@router.post("/create-checkout-session")
async def create_checkout_session(req: CheckoutSessionRequest):
    """Create a Stripe checkout session, or return a sandbox response."""
    if stripe is None or not os.getenv("STRIPE_SECRET_KEY"):
        return {
            "checkout_url": (
                "https://mrg-simulation-grid.fly.dev/pricing"
                f"?sandbox=1&user={req.user_id}"
            ),
            "mode": "sandbox",
            "message": "Stripe is not configured",
        }

    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": req.price_id, "quantity": 1}],
            mode="subscription" if "sub" in req.price_id else "payment",
            success_url=(
                "https://mrg-simulation-grid.fly.dev/dashboard"
                "?session_id={CHECKOUT_SESSION_ID}"
            ),
            cancel_url="https://mrg-simulation-grid.fly.dev/pricing",
            client_reference_id=req.user_id,
        )
        return {"checkout_url": session.url}
    except Exception as exc:  # pragma: no cover - external Stripe integration
        raise HTTPException(status_code=502, detail="Stripe checkout unavailable") from exc


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: Optional[str] = Header(None, alias="stripe-signature"),
):
    """Verify Stripe webhook signatures before handling billing events."""
    if stripe is None or not ENDPOINT_SECRET:
        return {"status": "ignored", "reason": "stripe_not_configured"}
    if not stripe_signature:
        raise HTTPException(status_code=400, detail="Missing Stripe signature.")

    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(payload, stripe_signature, ENDPOINT_SECRET)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid payload.") from exc
    except Exception as exc:  # Stripe SDK signature exception differs across versions.
        raise HTTPException(status_code=400, detail="Invalid Stripe signature.") from exc

    event_type = event["type"]
    session = event["data"]["object"]
    user_id = session.get("client_reference_id")

    if event_type == "checkout.session.completed":
        print(f"[BILLING] Activation verified for user: {user_id}")
    elif event_type in ("customer.subscription.deleted", "invoice.payment_failed"):
        print(f"[BILLING] Deactivation verified for user: {user_id}")

    return {"status": "success"}
