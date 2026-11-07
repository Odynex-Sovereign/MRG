import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response

HTTP_REQUESTS_TOTAL = Counter("mrg_http_requests_total", "HTTP Requests.", ["method", "endpoint", "status"])
REQUEST_DURATION = Histogram("mrg_request_duration_seconds", "Latency.", ["method", "endpoint"])

async def prometheus_metrics_middleware(request: Request, call_next):
    if request.url.path == "/metrics":
        return await call_next(request)
    start = time.time()
    response = await call_next(request)
    HTTP_REQUESTS_TOTAL.labels(method=request.method, endpoint=request.url.path, status=response.status_code).inc()
    REQUEST_DURATION.labels(method=request.method, endpoint=request.url.path).observe(time.time() - start)
    return response

def expose_metrics_endpoint():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
