import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="MRG — Integrated Simulation Suite")

# Get the absolute path to the directory containing this main.py file
# This ensures paths work perfectly both locally and inside the Fly.io Docker container
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Point directly to the root-level directories
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Mount static files safely (only if the directory exists to prevent crash)
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Configure Jinja2 template engine
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/", response_class=HTMLResponse)
async def read_landing(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/pricing", response_class=HTMLResponse)
async def read_pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})

@app.get("/onboarding", response_class=HTMLResponse)
async def read_onboarding(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})

@app.get("/demo", response_class=HTMLResponse)
async def read_demo(request: Request):
    return templates.TemplateResponse("demo.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/institutions", response_class=HTMLResponse)
async def read_institutions(request: Request):
    return templates.TemplateResponse("institutions.html", {"request": request})

@app.get("/healthz")
async def health_check():
    return {"status": "ok", "version": "2.0.0"}

@app.get("/readyz")
async def readiness_check():
    return {"status": "ready"}
