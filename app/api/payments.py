from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Dict, Any
from services.checkout_engine import UnifiedCheckoutEngine

router = APIRouter(prefix="/api/payments", tags=["Payments"])

# Re-use engine instance across routes
def get_checkout_engine() -> UnifiedCheckoutEngine:
    return UnifiedCheckoutEngine()

class PayPalCheckoutRequest(BaseModel):
    amount: float
    payment_method_nonce: str

@router.get("/paypal-token", response_model=Dict[str, str])
async def get_paypal_token(engine: UnifiedCheckoutEngine = Depends(get_checkout_engine)):
    """
    Generates a secure client token to initialization PayPal components safely on the frontend.
    """
    token = await engine.generate_paypal_client_token()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="PayPal/Braintree processing layer is unconfigured or offline."
        )
    return {"client_token": token}

@router.post("/paypal-checkout", response_model=Dict[str, Any])
async def paypal_checkout(
    payload: PayPalCheckoutRequest,
    engine: UnifiedCheckoutEngine = Depends(get_checkout_engine)
):
    """
    Receives the authorization nonce from the client window and executes the charge legally.
    """
    if payload.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction amount must be greater than zero."
        )

    result = await engine.process_paypal_sale(
        amount=payload.amount,
        payment_method_nonce=payload.payment_method_nonce
    )

    if result["status"] == "success":
        return result
        
    raise HTTPException(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        detail=result.get("error", "Transaction declined by alternative gateway.")
    )
