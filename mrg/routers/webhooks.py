import stripe
from fastapi import APIRouter, Request, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from mrg.core.config import settings
from mrg.core.database import get_db, UserSubscription

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None), db: Session = Depends(get_db)):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(payload, stripe_signature, settings.STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="Signature failed.")

    data_obj = event['data']['object']
    if event['type'] in ["checkout.session.completed", "invoice.payment_succeeded"]:
        user_id = data_obj.get("client_reference_id") or data_obj.get("metadata", {}).get("user_id")
        if user_id:
            sub = db.query(UserSubscription).filter(UserSubscription.user_id == user_id).first()
            if not sub:
                sub = UserSubscription(user_id=user_id)
                db.add(sub)
            sub.plan_tier = data_obj.get("metadata", {}).get("plan_tier", "Personal")
            sub.status = "active"
            db.commit()
    return {"status": "success"}
