from fastapi import APIRouter, Depends, HTTPException, status
from services.email_gateway import EnterpriseEmailGateway, IncomingEmailPayload

router = APIRouter(prefix="/api/v1/email-gateway", tags=["Automated Email Ingestion"])

def get_email_gateway() -> EnterpriseEmailGateway:
    from app import db_client, global_procurement_crawler
    return EnterpriseEmailGateway(db_client=db_client, crawler_engine=global_procurement_crawler)

@router.post("/inbound-webhook", status_code=status.HTTP_200_OK)
async def handle_inbound_mail_stream(
    payload: IncomingEmailPayload,
    gateway: EnterpriseEmailGateway = Depends(get_email_gateway)
):
    """
    Public webhook receiver for incoming B2B traffic relays.
    Parses metadata frames to trigger hands-free enterprise subscription sales.
    """
    try:
        result = await gateway.process_inbound_email_webhook(payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
