import os
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "https://fly.dev")

# Mapping your local mrg/core/pricing.py tiers to active Stripe Price IDs
STRIPE_PRICE_MAPPING = {
    "Personal": os.getenv("STRIPE_PRICE_PERSONAL"),
    "Household": os.getenv("STRIPE_PRICE_HOUSEHOLD"),
    "Pro": os.getenv("STRIPE_PRICE_PRO"),
    "Team": os.getenv("STRIPE_PRICE_TEAM"),
}

def create_production_checkout(user_id: str, plan_name: str, customer_email: str = None):
    price_id = STRIPE_PRICE_MAPPING.get(plan_name)
    if not price_id:
        raise ValueError(f"No live production price ID found configured for tier: {plan_name}")
    
    checkout_session = stripe.checkout.Session.create(
        customer_email=customer_email,
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=f"{PUBLIC_BASE_URL}/dashboard?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{PUBLIC_BASE_URL}/pricing",
        client_reference_id=user_id,
        metadata={
            "user_id": user_id,
            "plan_tier": plan_name
        }
    )
    return checkout_session.url

def create_customer_portal(stripe_customer_id: str):
    portal_session = stripe.billing_portal.Session.create(
        customer=stripe_customer_id,
        return_url=f"{PUBLIC_BASE_URL}/dashboard",
    )
    return portal_session.url
