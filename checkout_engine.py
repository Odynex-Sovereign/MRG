import logging
from typing import Dict, Any, Optional
import stripe
import braintree
from app.config import settings

logger = logging.getLogger("mrg.services.checkout_engine")

class UnifiedCheckoutEngine:
    """
    Legally handles multi-gateway transaction routing for the MRG suite.
    Binds Stripe and Braintree (PayPal/Venmo) under a clean processing interface.
    """
    def __init__(self):
        # 1. Initialize Stripe Configuration
        self.stripe_api_key = getattr(settings, "STRIPE_API_KEY", None)
        if self.stripe_api_key:
            stripe.api_key = self.stripe_api_key
            self.stripe_active = True
        else:
            logger.warning("[MRG Checkout] Stripe API key missing. Stripe processing disabled.")
            self.stripe_active = False

        # 2. Initialize Braintree/PayPal Configuration
        self.braintree_env = getattr(settings, "BRAINTREE_ENVIRONMENT", "sandbox")
        self.merchant_id = getattr(settings, "BRAINTREE_MERCHANT_ID", None)
        self.public_key = getattr(settings, "BRAINTREE_PUBLIC_KEY", None)
        self.private_key = getattr(settings, "BRAINTREE_PRIVATE_KEY", None)

        if all([self.merchant_id, self.public_key, self.private_key]):
            is_prod = self.braintree_env.lower() == "production"
            self.braintree_gateway = braintree.BraintreeGateway(
                braintree.Configuration(
                    environment=braintree.Environment.Production if is_prod else braintree.Environment.Sandbox,
                    merchant_id=self.merchant_id,
                    public_key=self.public_key,
                    private_key=self.private_key
                )
            )
            self.braintree_active = True
        else:
            logger.warning("[MRG Checkout] Braintree credentials incomplete. PayPal processing disabled.")
            self.braintree_active = False

    # ==========================================
    # STRIPE GATEWAY OPERATIONS
    # ==========================================
    async def create_stripe_checkout_session(self, price_id: str, client_id: str, success_url: str, cancel_url: str) -> Dict[str, Any]:
        """
        Generates a legally compliant hosted Stripe Checkout checkout session.
        Deflects card handling compliance away from local Fly machines.
        """
        if not self.stripe_active:
            return {"status": "error", "message": "Stripe processing layer is currently unconfigured."}

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription' if "sub" in price_id else 'payment',
                client_reference_id=client_id,
                success_url=success_url,
                cancel_url=cancel_url,
            )
            return {"status": "success", "url": session.url, "session_id": session.id}
        except Exception as e:
            logger.error(f"[Stripe Error] Failed to spin up checkout vault path: {str(e)}")
            return {"status": "error", "message": str(e)}

    # ==========================================
    # BRAINTREE / PAYPAL GATEWAY OPERATIONS
    # ==========================================
    async def generate_paypal_client_token(self) -> Optional[str]:
        """
        Generates a token required by the frontend client to securely initialization
        the PayPal/Venmo interface without exposing credentials.
        """
        if not self.braintree_active:
            return None
        try:
            return self.braintree_gateway.client_token.generate()
        except Exception as e:
            logger.error(f"[Braintree Error] Failed to build client initialization token: {str(e)}")
            return None

    async def process_paypal_sale(self, amount: float, payment_method_nonce: str) -> Dict[str, Any]:
        """
        Legally settles alternative currency transactions.
        Uses single-use payment nonces to securely move funds from a client wallet.
        """
        if not self.braintree_active:
            return {"status": "error", "message": "Braintree/PayPal processing layer unconfigured."}

        try:
            result = self.braintree_gateway.transaction.sale({
                "amount": f"{amount:.2f}",
                "payment_method_nonce": payment_method_nonce,
                "options": {
                    "submit_for_settlement": True
                }
            })

            if result.is_success:
                logger.info(f"[MRG PayPal Success] Settled transaction: {result.transaction.id}")
                return {
                    "status": "success",
                    "transaction_id": result.transaction.id,
                    "method": result.transaction.payment_instrument_type,
                    "amount": float(result.transaction.amount)
                }
            else:
                logger.error(f"[MRG PayPal Denied] Refused transaction processing: {result.message}")
                return {"status": "failed", "error": result.message}
                
        except Exception as e:
            logger.error(f"[Braintree Exception] Processing loop execution fault: {str(e)}")
            return {"status": "error", "message": str(e)}
