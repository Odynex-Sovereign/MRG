# MRG — Production Crisis Simulation Suite

**Deploy planet-scale crisis simulation digital twins with secure billing infrastructure.**

MRG is an enterprise-ready simulation suite designed to test composure and state validation under extreme stress, featuring PostgreSQL orchestration, real-time WebSocket telemetry, and Stripe subscription settlement.

## Quick Start & Verification

```bash
git clone <this-repo> && cd MRG
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

## Application Architecture

The repository isolates components across entrypoints, core logic, routing, and services:
* **`main.py`**: App entrypoint, middleware, and template mounting.
* **`core/`**: Environment security (`config.py`), SQLAlchemy database management (`database.py`), Stripe adapters (`billing.py`), and JWT security hooks (`security.py`).
* **`routers/`**: Asynchronous Stripe webhooks (`webhooks.py`) and high-frequency WebSocket telemetry routes (`simulation.py`).
* **`services/`**: State simulation metrics broadcast engine.

## Environment Configuration

Configure essential production variables:
* **`ENVIRONMENT`**: Operations context (`production`)
* **`SECRET_KEY`**: Cryptographic JWT signature (32-byte hex string)
* **`DATABASE_URL`**: PostgreSQL connection string
* **`STRIPE_SECRET_KEY` & `STRIPE_WEBHOOK_SECRET`**: Live Stripe settlement and webhook verification keys.

## Fly.io Deployment

Provision storage volumes, attach PostgreSQL databases, set encrypted secrets, and deploy:

```bash
fly volumes create mrg_storage --region iad --size 10
fly postgres attach --app mrg
fly secrets set SECRET_KEY="\$(openssl rand -hex 32)"
fly secrets set STRIPE_SECRET_KEY="sk_live_..."
fly secrets set STRIPE_WEBHOOK_SECRET="whsec_..."
fly deploy
```

Verify your deployment health:
```bash
curl -s https://fly.dev
```

## Quality Assurance

Run code linting and test suites:
```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
pytest--verbose
```
