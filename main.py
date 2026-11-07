from fastapi import FastAPI, Depends, HTTPException, status
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
from app.database.models import DBMeteredUsage
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
    """
    Creates a secure, itemized billing collection tunnel and 
    redirects the user straight to an input card payment window.
    """
    tenant_id = request.headers.get("X-Tenant-ID", "sandbox_default_user")
    
    price_map = {
        "growth": {"name": "MRG Growth Tier Subscription", "amount": 25000},  # $250.00
        "enterprise": {"name": "MRG Enterprise Core Grid", "amount": 95000}   # $950.00
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
