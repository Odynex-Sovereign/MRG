# ==========================================
# STAGE 1: Base Environment Setup
# ==========================================
FROM python:3.11-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app


# ==========================================
# STAGE 2: Local Development Sandbox (Target: development)
# ==========================================
FROM base AS development
CMD ["sh", "-c", "exec python -m uvicorn mrg.main:app --host 0.0.0.0 --port ${PORT:-8000} --reload"]


# ==========================================
# STAGE 3: Production Cloud Delivery (Target: production)
# ==========================================
FROM base AS production
# Run the documented production application, not the legacy streaming prototype.
CMD ["sh", "-c", "exec python -m uvicorn mrg.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
