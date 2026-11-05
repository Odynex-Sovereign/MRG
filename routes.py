from fastapi import APIRouter, HTTPException, Body
from checkout_engine import create_stripe_checkout_session

router = APIRouter()

@router.post("/api/checkout")
async def handle_checkout(payload: dict = Body(...)):
    """
    Endpoint that processes the 'Deploy License' requests from the UI.
    """
    # Extract structural pricing and routing parameters from the UI
    price_id = payload.get("price_id", "price_default_placeholder")
    base_url = payload.get("base_url", "https://mrg.fly.dev")
    
    success_route = f"{base_url}/success"
    cancel_route = f"{base_url}/pricing"
    
    # Process the session creation cleanly
    result = create_stripe_checkout_session(
        price_id=price_id,
        success_url=success_route,
        cancel_url=cancel_route,
        mode="subscription"
    )
    
    return result
