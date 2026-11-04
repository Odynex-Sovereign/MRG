FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 1. Copy over your project dependencies mapping manifest
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Drop the full package codebase into the container runtime
COPY . .

EXPOSE 8000

# 3. CRITICAL FIX: Explicitly inject Python module system paths 
# This tells Uvicorn to use the current directory root as its module base
ENV PYTHONPATH=/app

# 4. Fire up the application loop bound to the global 0.0.0.0 network adapter
CMD ["python", "-m", "uvicorn", "services.streaming.websocket_pipeline:app", "--host", "0.0.0.0", "--port", "8000"]
