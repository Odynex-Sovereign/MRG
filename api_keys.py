import secrets
import hashlib
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/keys", tags=["Developer Access"])

class KeyGenerationRequest(BaseModel):
    user_id: str
    assigned_label: str

@router.post("/generate")
async def issue_developer_key(req: KeyGenerationRequest):
    # Generates standard secure cryptographically random tokens
    raw_token = "mrg_live_" + secrets.token_hex(24)
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
    
    return {
        "api_key": raw_token,
        "key_prefix": raw_token[:12],
        "hashed_reference": hashed_token,
        "assigned_label": req.assigned_label,
        "rate_limit_per_minute": 120,
        "status": "Active"
  }
