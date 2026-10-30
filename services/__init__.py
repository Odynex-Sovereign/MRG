# System initialization layer linking auth, keys, and streaming logic routers
from services.auth.routes import router as auth_router
from services.auth.api_keys import router as api_keys_router
from services.streaming.websocket_pipeline import app

# Include explicit REST endpoints into the global FastAPI micro-VM context
app.include_router(auth_router)
app.include_router(api_keys_router)
