import os
import stripe
from fastapi import HTTPException

# Initialize Stripe API Key safely from environment variables
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_stripe_checkout_session(price_id: str, success_url: str, cancel_url: str, mode: str = "subscription") -> dict:
    """
    Safely creates a Stripe Checkout Session and returns the direct redirect URL.
    Falls back gracefully if the API keys are not supplied.
    """
    if not stripe.api_key or stripe.api_key.startswith("demo_"):
        # Graceful fallback placeholder if keys aren't set yet
        return {
            "url": f"{success_url}?session_id=mock_sandbox_session_success"
        }

    try:
        # Generate the verified Stripe session
        session = stripe.checkout.sessions.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode=mode,
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
        )
        
        # Explicitly return the structural dictionary with the valid URL string
        return {"url": session.url}

    except stripe.error.StripeError as e:
        # Break the error loop and bubble up the real Stripe error payload
        raise HTTPException(
            status_code=400, 
            detail=f"Stripe API Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Internal Checkout Generation Failure: {str(e)}"
     )
