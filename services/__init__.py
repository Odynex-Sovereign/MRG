"""Application package and router registration."""

from services.auth.api_keys import router as api_keys_router
from services.auth.billing import router as billing_router
from services.auth.routes import router as auth_router
from services.streaming.websocket_pipeline import app

app.include_router(auth_router)
app.include_router(api_keys_router)
app.include_router(billing_router)

__all__ = ["app"]
