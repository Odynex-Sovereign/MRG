from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db_client import get_db
from deepseek_client import generate_macro_ripple

router = APIRouter()

@router.get("/healthz")
async def health_check():
    return {"status": "healthy", "engine": "MRG Planet-Scale Grid"}

@router.post("/simulate/macro")
async def trigger_macro_simulation(prompt: str, db: Session = Depends(get_db)):
    ripple_effect = await generate_macro_ripple(prompt)
    return {"success": True, "analysis": ripple_effect}
