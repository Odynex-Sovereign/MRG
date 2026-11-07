import os
import stripe
from fastapi import APIRouter, Request, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from mrg.core.database import get_db, UserSubscription

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/stripe")
async def stripe_webhook(
    request: Request, 
    stripe_signature: str = Header(None), 
    db: Session = Depends(get_db)
):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        raise HTTPException(status_code=400, detail="Invalid signature verification.")

    event_type = event['type']
    data_object = event['data']['object']

    if event_type in ["checkout.session.completed", "invoice.payment_succeeded"]:
        user_id = data_object.get("client_reference_id") or data_object.get("metadata", {}).get("user_id")
        customer_id = data_object.get("customer")
        subscription_id = data_object.get("subscription")
        
        # Determine plan tier via metadata setup
        plan_tier = data_object.get("metadata", {}).get("plan_tier", "Personal")

        if user_id:
            sub = db.query(UserSubscription).filter(UserSubscription.user_id == user_id).first()
            if not sub:
                sub = UserSubscription(user_id=user_id)
                db.add(sub)
            
            sub.stripe_customer_id = customer_id
            sub.stripe_subscription_id = subscription_id
            sub.plan_tier = plan_tier
            sub.status = "active"
            db.commit()

    elif event_type == "customer.subscription.deleted":
        sub_id = data_object.get("id")
        sub = db.query(UserSubscription).filter(UserSubscription.stripe_subscription_id == sub_id).first()
        if sub:
            sub.plan_tier = "Free"
            sub.status = "canceled"
            db.commit()

    return {"status": "success"}
