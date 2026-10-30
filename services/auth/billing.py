import os
import stripe
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from pydantic import BaseModel 

router = APIRouter(prefix="/api/billing", tags=["Billing & Monetization"]) 

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
ENDPOINT_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET") 

class CheckoutSessionRequest(BaseModel):
user_id: str
price_id: str  # Stripe Price ID matching Tier 1, Tier 2, or Tier 3 

@router.post("/create-checkout-session")
async def create_checkout_session(req: CheckoutSessionRequest):
"""
Generates a secure checkout link for Odynex Axis Logistics monetization tiers.
"""
try:
session = stripe.checkout.Session.create(
payment_method_types=['card'],
line_items=[{"price": req.price_id, "quantity": 1}],
mode="subscription" if "sub" in req.price_id else "payment",
success_url="https://mrg-simulation-grid.fly.dev/dashboard?session_id={CHECKOUT_SESSION_ID}",
cancel_url="https://mrg-simulation-grid.fly.dev/pricing",
client_reference_id=req.user_id,
)
return {"checkout_url": session.url}
except Exception as e:
raise HTTPException(status_code=500, detail=f"Stripe initialization error: {e}") 

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
"""
Listens directly to Stripe infrastructure events to provision or revoke simulation tiers.
"""
payload = await request.body()
try:
event = stripe.Webhook.construct_event(
payload, stripe_signature, ENDPOINT_SECRET
)
except ValueError:
raise HTTPException(status_code=400, detail="Invalid payload payload configuration.")
except stripe.error.SignatureVerificationError:
raise HTTPException(status_code=400, detail="Invalid signature profile verification.") 

event_type = event['type']
session = event['data']['object']
user_id = session.get('client_reference_id')

if event_type == "checkout.session.completed":

# logic loop to mark user as active and authorized within database

print(f"[BILLING] Activation verified for user: {user_id}")

elif event_type in ["customer.subscription.deleted", "invoice.payment_failed"]:
# logic loop to drop active simulation authorization bounds
print(f"[BILLING] Deactivation verified for user: {user_id}") 

return {"status": "success"}
