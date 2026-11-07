from fastapi import APIRouter, Response, HTTPException
from mrg.services import mock_data

router = APIRouter(prefix="/api/industrial", tags=["enterprise-mesh"])

@router.get("/nasdaq/feed", response_class=Response)
async def get_nasdaq_binary_packet_feed():
    """Serves high-frequency binary packet blocks structured on low-latency asset network protocols."""
    if not mock_data.LATEST_NASDAQ_MARKET_STREAM:
        raise HTTPException(status_code=503, detail="Financial data stream initialization pending.")
    
    return Response(
        content=mock_data.LATEST_NASDAQ_MARKET_STREAM, 
        media_type="application/octet-stream"
    )

@router.get("/siemens/twin", response_class=Response)
async def get_siemens_twin_node_payload():
    """Serves state verification payloads matching Siemens Industrial Edge bindings."""
    return Response(
        content=mock_data.LATEST_SIEMENS_TWIN_NODE,
        media_type="application/json"
  )
