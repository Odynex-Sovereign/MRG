from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from mrg.core.config import settings
from mrg.core.database import init_db
from mrg.routers import webhooks, simulation
from mrg.core.billing import create_production_checkout

app = FastAPI(title="MRG Grid Operating System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="mrg/static"), name="static")
templates = Jinja2Templates(directory="mrg/templates")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(webhooks.router)
app.include_router(simulation.router)

@app.get("/pricing", response_class=HTMLResponse)
def get_pricing_page(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})

@app.post("/api/billing/checkout")
async def target_checkout_session(user_id: str, plan_tier: str, email: str = None):
    try:
        checkout_url = create_production_checkout(user_id=user_id, plan_name=plan_tier, customer_email=email)
        return {"url": checkout_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/healthz")
def health_check():
    return {"status": "ok", "version": "2.0.0"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from mrg.core.config import settings
from mrg.core.database import init_db
from mrg.routers import webhooks, simulation, auth

app = FastAPI(title="MRG Grid Operating System Matrix")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="mrg/static"), name="static")
templates = Jinja2Templates(directory="mrg/templates")

@app.on_event("startup")
def on_startup():
    init_db()

# Mount all unified operational endpoint domains
app.include_router(webhooks.router)
app.include_router(simulation.router)
app.include_router(auth.router)

@app.get("/pricing", response_class=HTMLResponse)
def get_pricing_page(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})

@app.get("/healthz")
def health_check():
    return {"status": "ok", "version": "2.0.0"}
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from mrg.core.config import settings
from mrg.core.database import init_db
from mrg.routers import webhooks, simulation, auth, pages
from mrg.services.mock_data import generate_continuous_validation_metrics

app = FastAPI(title="MRG Grid Operating System Matrix Hub")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="mrg/static"), name="static")

@app.on_event("startup")
def on_startup():
    # Initialize live physical database connections
    init_db()
    
    # Fire up the continuous validation mock data monitoring engine in the background loop
    asyncio.create_task(generate_continuous_validation_metrics())

# Mount unified frontend templates, security networks, and background worker engines
app.include_router(pages.router)
app.include_router(webhooks.router)
app.include_router(simulation.router)
app.include_router(auth.router)

@app.get("/healthz")
def health_check():
    return {"status": "ok", "version": "2.0.0"}

@app.get("/readyz")
def readiness_check():
    return {"status": "ready"}
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from mrg.core.config import settings
from mrg.core.database import init_db
from mrg.routers import webhooks, simulation, auth, pages, industrial
from mrg.services.mock_data import generate_continuous_validation_metrics

app = FastAPI(title="MRG High-Performance Resilient Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="mrg/static"), name="static")

@app.on_event("startup")
def on_startup():
    # Initialize physical persistent database engine maps
    init_db()
    
    # Launch the synchronized background simulation worker array
    asyncio.create_task(generate_continuous_validation_metrics())

# Mount endpoint modules
app.include_router(pages.router)
app.include_router(industrial.router)
app.include_router(webhooks.router)
app.include_router(simulation.router)
app.include_router(auth.router)

@app.get("/healthz")
def health_check():
    return {"status": "ok", "version": "2.0.0"}
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from mrg.core.config import settings
from mrg.core.database import init_db
from mrg.routers import webhooks, simulation, auth, pages, industrial, alerts
from mrg.services.mock_data import generate_continuous_validation_metrics

app = FastAPI(title="MRG Mission Critical Grid Hub")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="mrg/static"), name="static")

@app.on_event("startup")
def on_startup():
    # Structural database layout setup
    init_db()
    
    # Asynchronous worker initialization
    asyncio.create_task(generate_continuous_validation_metrics())

# Route Configuration Registries
app.include_router(pages.router)
app.include_router(industrial.router)
app.include_router(alerts.router)
app.include_router(webhooks.router)
app.include_router(simulation.router)
app.include_router(auth.router)

@app.get("/healthz")
def health_check():
    return {"status": "ok", "version": "2.0.0"}
