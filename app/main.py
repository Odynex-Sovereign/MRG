from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os
import stripe

from app.core.config import settings
from app.middleware.metering import SimulationMeteringMiddleware
from app.database.session import get_db
from app.database.models import DBMeteredUsage, DBSubscription
from app.services.export_engine import usage_export_engine

stripe.api_key = settings.STRIPE_SECRET_KEY

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SimulationMeteringMiddleware)

os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    if os.path.exists("templates/index.html"):
        return templates.TemplateResponse("index.html", {"request": request})
    return HTMLResponse("<h1>MRG Core Engine Running Containerized</h1>")

@app.get("/health", status_code=200)
async def health_check():
    return {"status": "healthy", "pipeline": "metered_revenue"}

@app.get("/api/v1/billing/checkout")
async def create_checkout_session(request: Request, tier: str = "growth"):
    tenant_id = request.headers.get("X-Tenant-ID", "sandbox_default_user")
    
    price_map = {
        "growth": {"name": "MRG Growth Tier Subscription", "amount": 29900},      # $299.00
        "enterprise": {"name": "MRG Enterprise Core Grid", "amount": 99900}     # $999.00
    }
    
    selected_plan = price_map.get(tier.lower(), price_map["growth"])
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': selected_plan["name"]},
                    'unit_amount': selected_plan["amount"],
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{settings.DOMAIN_URL}?session=success&tenant={tenant_id}",
            cancel_url=f"{settings.DOMAIN_URL}?session=cancelled",
            metadata={"tenant_id": tenant_id, "tier_selection": tier}
        )
        return RedirectResponse(url=checkout_session.url, status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Stripe processing layer initialization failed: {str(e)}"
        )

@app.post("/api/v1/billing/webhook")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Cryptographically verifies inbound event signatures directly from Stripe.
    Fulfills company orders and updates customer tier allocations asynchronously.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid request payload structure.")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Cryptographic webhook signature verify mismatch.")

    # Core Event Processing Hook
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        
        # Extract target meta tracking entities attached at request initialization
        tenant_id = session["metadata"].get("tenant_id")
        tier_selection = session["metadata"].get("tier_selection", "growth").capitalize()
        
        if tenant_id:
            # Upsert the subscription allocation records straight into your Postgres engine matrix
            result = await db.execute(select(DBSubscription).where(DBSubscription.tenant_id == tenant_id))
            db_sub = result.scalars().first()
            
            max_seats = 50 if tier_selection.lower() == "enterprise" else 10
            
            if not db_sub:
                db_sub = DBSubscription(tenant_id=tenant_id)
                db.add(db_sub)
                
            db_sub.tier_name = tier_selection
            db_sub.max_seats = max_seats
            db_sub.is_active = True
            
            await db.commit()
            print(f"[REVENUE_SUCCESS] Tenant {tenant_id} upgraded cleanly to {tier_selection}.")

    return {"status": "event_processed_successfully"}

@app.get("/api/v1/billing/export")
async def export_billing_ledger(request: Request, db: AsyncSession = Depends(get_db)):
    tenant_id = request.headers.get("X-Tenant-ID", "sandbox_default_user")
    try:
        result = await db.execute(
            select(DBMeteredUsage)
            .where(DBMeteredUsage.tenant_id == tenant_id)
            .order_by(DBMeteredUsage.timestamp.desc())
        )
        entries = result.scalars().all()
        csv_data = usage_export_engine.generate_csv_report(entries)
        filename = f"mrg_billing_ledger_{tenant_id}.csv"
        return StreamingResponse(
            iter([csv_data]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate financial ledger stream: {str(e)}"
)
