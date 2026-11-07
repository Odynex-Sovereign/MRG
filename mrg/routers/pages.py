from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from mrg.core.security import get_current_user_id

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="mrg/templates")

@router.get("/", response_class=HTMLResponse)
def render_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "MRG Platform"})

@router.get("/pricing", response_class=HTMLResponse)
def render_pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})

@router.get("/demo", response_class=HTMLResponse)
def render_demo(request: Request, user_id: str = Depends(get_current_user_id)):
    return templates.TemplateResponse("demo.html", {"request": request, "user_id": user_id})

@router.get("/onboarding", response_class=HTMLResponse)
def render_onboarding(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})
