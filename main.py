import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="MRG — Integrated Simulation Suite")

# Define base paths relative to the application route
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Correctly mount your static asset folder for CSS/JS
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Instantiate Jinja2 Template directory mapping
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_landing(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/pricing", response_class=HTMLResponse)
async def read_pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})

# FIX: Added explicit template router endpoint for onboarding page
@app.get("/onboarding", response_class=HTMLResponse)
async def read_onboarding(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/institutions", response_class=HTMLResponse)
async def read_institutions(request: Request):
    return templates.TemplateResponse("institutions.html", {"request": request})

@app.get("/healthz")
async def health_check():
    return {"status": "ok", "version": "2.0.0"}
