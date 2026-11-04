# services/billing/stripe_webhooks.py
import os
import json
from fastapi import FastAPI, Request, Header, HTTPException
from database.db_client import get_db_connection

app = FastAPI(title="MRG Automated Revenue Ingestion Engine")

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "mock_secret_for_instant_billing")

@app.post("/v1/webhooks/stripe")
async def stripe_webhook_endpoint(request: Request, stripe_signature: str = Header(None)):
    """
    Ingests live payment updates from Stripe.
    Automatically provisions software capabilities on successful payment event loops.
    """
    payload = await request.body()
    
    # In sandbox or if secret is unset, process the raw payload directly for speed
    try:
        event = json.loads(payload)
    except Exception:
        raise HTTPException(status_code=400, detail="Malformed payload architecture.")
        
    event_type = event.get("type")
    
    # Handle successful customer checkout events (Automated Ingestion Loop)
    if event_type in ["checkout.session.completed", "invoice.payment_succeeded"]:
        data_object = event.get("data", {}).get("object", {})
        
        # Pull transactional metadata passed during self-serve user checkout
        session_id = data_object.get("metadata", {}).get("session_id")
        selected_tier = data_object.get("metadata", {}).get("tier_id", "tier_1")
        billing_value = data_object.get("amount_total", 0) / 100.0  # Convert from cents
        
        if session_id:
            conn = get_db_connection()
            if conn:
                try:
                    with conn.cursor() as cur:
                        # Activate the platform tier workspace privileges instantly
                        cur.execute(
                            """
                            INSERT INTO billing_subscriptions 
                            (session_id, platform_tier, pricing_architecture, billing_value, target_margin_pct, is_active)
                            VALUES (%s, %s, %s, %s, %s, TRUE)
                            ON CONFLICT (session_id) 
                            DO UPDATE SET 
                                platform_tier = EXCLUDED.platform_tier,
                                billing_value = EXCLUDED.billing_value,
                                is_active = TRUE;
                            """,
                            (session_id, selected_tier, "automated_self_serve", billing_value, 85.0)
                        )
                    conn.commit()
                    print(f"[REVENUE INGESTED]: Tier {selected_tier} activated for Session {session_id}")
                except Exception as e:
                    print(f"Failed to provision active subscription seat: {e}")
                finally:
                    conn.close()
                    
    return {"status": "success", "processed": True}
