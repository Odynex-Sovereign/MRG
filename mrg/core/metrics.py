import time
from fastapi import Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

# Core Monitoring Observability Vectors
HTTP_REQUESTS_TOTAL = Counter(
    "mrg_http_requests_total", 
    "Total number of processed HTTP requests.", 
    ["method", "endpoint", "http_status"]
)

REQUEST_DURATION_SECONDS = Histogram(
    "mrg_request_duration_seconds", 
    "HTTP Request Latency Distribution in seconds.", 
    ["method", "endpoint"]
)

async def prometheus_metrics_middleware(request: Request, call_next):
    """Intercepts request-response pathways non-blockingly to log execution timelines."""
    if request.url.path == "/metrics":
        return await call_next(request)
        
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    HTTP_REQUESTS_TOTAL.labels(
        method=request.method, 
        endpoint=request.url.path, 
        http_status=response.status_code
    ).inc()
    
    REQUEST_DURATION_SECONDS.labels(
        method=request.method, 
        endpoint=request.url.path
    ).observe(duration)
    
    return response

def expose_metrics_endpoint():
    """Generates a text/plain response block parseable by scrapers."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
