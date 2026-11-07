from fastapi import APIRouter, Response
from mrg.services import mock_data

router = APIRouter(prefix="/api/industrial", tags=["industrial"])

@router.get("/nasdaq/feed")
async def get_nasdaq_feed():
    return Response(content=mock_data.LATEST_NASDAQ_MARKET_STREAM, media_type="application/octet-stream")

@router.get("/siemens/twin")
async def get_siemens_twin():
    return Response(content=mock_data.LATEST_SIEMENS_TWIN_NODE, media_type="application/json")
