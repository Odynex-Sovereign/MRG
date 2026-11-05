import os
import json
import stripe
from fastapi import APIRouter, Request, Header, HTTPException, Response

router = APIRouter()

# Initialize credentials from environment context
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
ENDPOINT_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/api/webhooks/stripe")
async def handle_stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    """
    Listens for real-time Stripe checkout and subscription events.
    Verifies payload authenticity and provisions simulation grid configurations.
    """
    payload = await request.body()
    
    # Handle development or missing credential fallbacks cleanly
    if not ENDPOINT_SECRET or ENDPOINT_SECRET.startswith("demo_"):
        try:
            event_data = json.loads(payload.decode('utf-8'))
            print("⚠️ WEBHOOK SANDBOX MODE: Skipping signature check.")
            await process_webhook_event(event_data.get("type"), event_data.get("data", {}).get("object", {}))
            return Response(content="Sandbox payload simulated successfully", status_code=200)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid unverified payload structure: {str(e)}")

    if not stripe_signature:
        raise HTTPException(status_code=400, detail="Missing required Stripe-Signature Header")

    # Secure verification phase using cryptographic signatures
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, ENDPOINT_SECRET
        )
    except ValueError as e:
        # Invalid payload structure
        raise HTTPException(status_code=400, detail="Invalid webhook payload format")
    except stripe.error.SignatureVerificationError as e:
        # Signature mismatch (e.g. key rotation or spoofing attempt)
        raise HTTPException(status_code=400, detail="Signature verification rejected")

    # Routing verified event structures
    event_type = event.get("type")
    event_object = event.get("data", {}).get("object", {})
    
    await process_webhook_event(event_type, event_object)
    
    return Response(content="Webhook event ingested successfully", status_code=200)


async def process_webhook_event(event_type: str, stripe_object: dict):
    """
    Asynchronous event router that handles state mutations based on finalized payments.
    """
    print(f"📦 Processing Stripe Event: {event_type}")

    if event_type == "checkout.session.completed":
        # Fires immediately when a customer finishes the Stripe Checkout workflow
        customer_email = stripe_object.get("customer_details", {}).get("email")
        subscription_id = stripe_object.get("subscription")
        session_id = stripe_object.get("id")
        
        print(f"✅ Success: Payment cleared for {customer_email}. Session: {session_id}")
        await provision_mrg_license(customer_email, subscription_id)

    elif event_type == "customer.subscription.deleted":
        # Fires immediately if a user cancels or their card declines repeatedly
        subscription_id = stripe_object.get("id")
        print(f"❌ Cancelled: Subscription {subscription_id} has expired.")
        await revoke_mrg_license(subscription_id)

    else:
        # Safe log for structural events you aren't listening for yet
        print(f"ℹ️ Unhandled hook notification: {event_type}")


async def provision_mrg_license(email: str, subscription_id: str):
    """
    Trigger your server's logic here to unlock simulation grids, send welcome emails, 
    or update your active database profiles.
    """
    # TODO: Add your custom database/simulation workspace generation strings here
    pass


async def revoke_mrg_license(subscription_id: str):
    """
    Trigger your server's logic here to cleanly teardown simulation instances
    when active subscriptions end.
    """
    # TODO: Add your custom database teardown/disable execution flows here
    pass
