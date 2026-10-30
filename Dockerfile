# Use an explicit, stable Python footprint matching MRG requirements
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Establish the workspace directory
WORKDIR /app

# Install system dependencies needed for runtime tooling and PostgreSQL networking
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to exploit Docker layer caching 
COPY requirements.txt .

# Install dependencies at the global scope cleanly
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire simulation grid codebase into the workspace
COPY . .

# Expose the internal network port configured in fly.toml
EXPOSE 8000

# CRITICAL FIX: Explicitly bind the host to 0.0.0.0 so the fly-proxy can pass health checks
CMD ["uvicorn", "services.streaming.websocket_pipeline:app", "--host", "0.0.0.0", "--port","8000"]
