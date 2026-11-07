from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from mrg.core.security import get_current_user_id

router = APIRouter(tags=["frontend-pages"])
templates = Jinja2Templates(directory="mrg/templates")

@router.get("/", response_class=HTMLResponse)
async def render_landing_page(request: Request):
    """Serves the central product overview dashboard and presentation interface."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "MRG Platform — Global Crisis Digital Twin Simulation Grid"
    })

@router.get("/demo", response_class=HTMLResponse)
async def render_sandbox_demo(request: Request, user_id: str = Depends(get_current_user_id)):
    """Serves the secure interactive telemetry sandbox testing stream interface."""
    return templates.TemplateResponse("demo.html", {
        "request": request,
        "user_id": user_id
    })

@router.get("/onboarding", response_class=HTMLResponse)
async def render_guided_onboarding(request: Request):
    """Serves the initial configuration workflow wizard for platform activation."""
    return templates.TemplateResponse("onboarding.html", {"request": request})
