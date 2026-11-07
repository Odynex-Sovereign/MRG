from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.billing_vault import billing_vault
import time

class SimulationMeteringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Identify tenant from security authorization headers or session cookies
        tenant_id = request.headers.get("X-Tenant-ID", "sandbox_default_user")
        
        # Simple checkpoint check for premium telemetry endpoint validation
        if request.url.path.startswith("/ws/simulation"):
            # Check if user has an active or delinquent subscription standing
            is_valid_standing = True # Query database layer in production
            if not is_valid_standing:
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED, 
                    detail="Simulation allocation limits exhausted. Upgrade to Growth Tier at ://mrg.com"
                )

        start_time = time.time()
        response = await call_next(request)
        duration_seconds = time.time() - start_time

        # If a valid streaming simulation loop just completed, meter it instantly
        if request.url.path.startswith("/ws/simulation") and response.status_code == 200:
            from app.models.billing import UsageMeter
            import uuid
            
            mock_usage = UsageMeter(
                tenant_id=tenant_id,
                session_id=str(uuid.uuid4()),
                simulation_minutes=round(duration_seconds / 60.0, 4),
                deepseek_tokens=int(duration_seconds * 15), # Approximate output density
                riva_audio_seconds=round(duration_seconds, 2)
            )
            await billing_vault.report_usage_event(mock_usage)

        return response
