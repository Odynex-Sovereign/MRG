from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, List
from services.billing_vault import AdvancedFinancialRouter

router = APIRouter(prefix="/api/marketplace", tags=["B2B Marketplace & Developer API"])

class VendorRegistrationRequest(BaseModel):
    vendor_name: str
    stripe_connect_id: str
    target_industry_vertical: str

class TokenDebitRequest(BaseModel):
    developer_secret_key: str
    data_packets_processed: int

def get_financial_router() -> AdvancedFinancialRouter:
    from app import db_client
    return AdvancedFinancialRouter(db_client=db_client)

@router.post("/register-vendor", response_model=Dict[str, str])
async def register_consultant_vendor(
    payload: VendorRegistrationRequest,
    finance_router: AdvancedFinancialRouter = Depends(get_financial_router)
):
    """
    Registers an external consulting firm onto the MRG grid mesh.
    Binds their merchant profile to Stripe Connect for autonomous platform fee routing.
    """
    try:
        await finance_router.db.execute(
            "INSERT INTO billing_vault (client_id, tier_level, active, ledger_balance) "
            "VALUES ($1, 'enterprise_elite', True, 0.00)", payload.stripe_connect_id
        )
        return {"status": "approved", "vendor_token": f"mrg_vendor_{uuid.uuid4().hex[:16]}"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/consume-api-telemetry", response_model=Dict[str, Any])
async def debit_headless_api_usage(
    payload: TokenDebitRequest,
    finance_router: AdvancedFinancialRouter = Depends(get_financial_router)
):
    """
    Headless API Gateway: Charges external enterprise developers on demand
    for pulling direct telemetry packets into their own internal dashboards.
    """
    result = await finance_router.charge_headless_api_token_consumption(
        developer_key=payload.developer_secret_key,
        data_packets_processed=payload.data_packets_processed
    )
    if result["status"] == "debited":
        return result
    raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Insufficient pre-funded API balance.")
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any
from services.billing_vault import AdvancedFinancialRouter

router = APIRouter(prefix="/api/marketplace", tags=["B2B Marketplace & Headless API"])

class VendorRegistrationRequest(BaseModel):
    vendor_name: str
    stripe_connect_id: str
    target_industry_vertical: str

class TokenDebitRequest(BaseModel):
    developer_secret_key: str
    data_packets_processed: int

def get_financial_router() -> AdvancedFinancialRouter:
    from app import db_client
    return AdvancedFinancialRouter(db_client=db_client)

@router.post("/register-vendor")
async def register_consultant_vendor(
    payload: VendorRegistrationRequest,
    finance_router: AdvancedFinancialRouter = Depends(get_financial_router)
):
    try:
        await finance_router.db.execute(
            "INSERT INTO billing_vault (client_id, tier_level, active, ledger_balance) "
            "VALUES ($1, 'enterprise_elite', True, 0.00)", payload.stripe_connect_id
        )
        return {"status": "approved", "vendor_token": f"mrg_vendor_{uuid.uuid4().hex[:16]}"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/consume-api-telemetry")
async def debit_headless_api_usage(
    payload: TokenDebitRequest,
    finance_router: AdvancedFinancialRouter = Depends(get_financial_router)
):
    result = await finance_router.charge_headless_api_token_consumption(
        developer_key=payload.developer_secret_key,
        data_packets_processed=payload.data_packets_processed
    )
    if result["status"] == "debited":
        return result
    raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Insufficient pre-funded API token balance.")
