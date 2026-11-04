# MRG Integrated Simulation Suite

[![CI](https://github.com/Odynex-Sovereign/MRG/actions/workflows/ci.yml/badge.svg)](https://github.com/Odynex-Sovereign/MRG/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)

**Planet-scale crisis simulation grid** combining long-horizon structural reasoning (DeepSeek), low-latency micro-conversational models (NVIDIA Nemotron / NIM), and sensory engines (Riva + Audio2Face) for executive stress-testing under extreme pressure.

---

## Features

- **WebSocket simulation channel** (`/ws/simulation`) — telemetry packets and crisis triggers
- **Macro-cognitive engine** — DeepSeek (or deterministic sandbox fallback)
- **Sensory stream stubs** — ready for NVIDIA Riva / Audio2Face wiring
- **Health probes** — `/healthz` (liveness), `/readyz` (readiness), `/info`
- **Structured JSON logging**, security headers, request timing
- **Optional PostgreSQL** for session telemetry and auth keys
- **Docker / Compose / Fly.io** production paths
- **CI** — lint, type-check, tests, container build on every PR

---

## Architecture

```
Client (browser / edge) ──WebSocket──► mrg.app (FastAPI)
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
              Macro service        Sensory service      Optional Postgres
            (DeepSeek / sandbox)  (Riva stub / mock)   (asyncpg pool)
```

See [docs/architecture.md](docs/architecture.md) for detail.

---

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (for full stack)
- Optional: `flyctl` for Fly.io deployment
- Optional API keys: DeepSeek, NVIDIA NIM, Livepeer, Stripe

---

## Local setup

```bash
git clone https://github.com/Odynex-Sovereign/MRG.git
cd MRG
python3.11 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
make install
cp .env.example .env        # edit if needed — keys optional
```

### Sandbox (no external services)

```bash
make sandbox
# → http://localhost:8000/docs
# → http://localhost:8000/healthz
```

### WebSocket smoke test (server running)

```bash
make smoke
# or: python tests/mock_client_test.py
```

### Full stack (Postgres + engine)

```bash
make docker-up
# wait for healthy
make migrate
make smoke
```

---

## Environment variables

See [`.env.example`](.env.example) for the full list. Critical ones:

| Variable | Required | Description |
|----------|----------|-------------|
| `ENVIRONMENT` | no | `development` / `staging` / `production` |
| `DATABASE_URL` | no | Postgres DSN; omit for pure sandbox |
| `DEEPSEEK_API_KEY` | no | Macro engine; sandbox fallback if empty |
| `NVIDIA_NIM_API_KEY` | no | Sensory / micro-tactical integrations |
| `CORS_ORIGINS` | no | Comma-separated or `*` |
| `LOG_FORMAT` | no | `json` (prod) or `text` |

**Never commit real secrets.** Use platform secret stores (Fly secrets, K8s secrets, etc.).

---

## Development workflow

```bash
make format      # ruff format + fix
make lint        # ruff check
make typecheck   # mypy
make test        # pytest
make test-cov    # coverage report
```

Pre-commit (optional):

```bash
pre-commit install
```

---

## Docker usage

```bash
docker compose up -d --build
curl http://localhost:8000/healthz
docker compose logs -f mrg
docker compose down
```

Image is multi-stage, non-root (`uid 10001`), uses `tini`, and includes a HEALTHCHECK.

---

## Production deployment

### Fly.io (recommended quick path)

```bash
fly launch --no-deploy --name <your-mrg-app>
fly secrets set DEEPSEEK_API_KEY=sk-... NVIDIA_NIM_API_KEY=nvapi-...
# optional: fly secrets set DATABASE_URL=postgresql://...
fly deploy
fly status
curl https://<app>.fly.dev/healthz
```

### Kubernetes

Manifests in `deploy/k8s/`. See [docs/deployment.md](docs/deployment.md).

### Terraform

Starter module in `deploy/terraform/`. Supply cloud credentials via env / OIDC — nothing is hardcoded.

---

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`):

1. **quality** — ruff, mypy, pytest + coverage on every PR / push
2. **docker** — build production image and smoke `/healthz`
3. **deploy** — `flyctl deploy` on `main` when `FLY_API_TOKEN` secret is present

---

## Security practices

- No secrets in repo; `.env` gitignored
- Non-root containers, read-only root filesystem in Compose
- Security headers middleware
- Input validation (Pydantic) and message size limits on WebSocket
- CORS and trusted-host configurable
- See [SECURITY.md](SECURITY.md) for reporting

---

## Monitoring, logging, troubleshooting

- Structured logs (JSON in production) to stdout — ship to your aggregator
- `/healthz` for liveness, `/readyz` for readiness (fails if DB configured but down)
- Slow-request warnings (>1s)
- Common issues: see [docs/runbook.md](docs/runbook.md) and [docs/operations.md](docs/operations.md)

---

## Scaling guidance

- Stateless app process — scale horizontally behind a load balancer that supports WebSockets
- Externalize state to Postgres / Redis (not yet required for core path)
- Tune `workers` / replica count based on concurrent WS connections
- DeepSeek / NIM rate limits are external constraints

---

## Backup, recovery, upgrade, rollback

- Postgres: use managed backups or `pg_dump`; volume `mrg_pgdata` for local Compose
- App: immutable images; rollback by redeploying previous image tag / Fly release
- Migrations are forward-only SQL files under `database/migrations/`

---

## Repository structure

```
mrg/                 # Production application package
  app.py             # FastAPI factory
  config.py          # Pydantic settings
  api/               # HTTP + WebSocket routers
  services/          # Macro / sensory domain logic
services/            # Legacy module layout (compat re-exports)
database/            # asyncpg helpers + SQL migrations
app/                 # Static HTML UI
config/              # JSON model manifests
deploy/              # K8s + Terraform starters
docs/                # Architecture, deployment, ops, runbook
tests/               # Unit + WebSocket tests
Dockerfile           # Multi-stage production image
docker-compose.yml   # Local prod-like stack
```

---

## License & contributing

MIT — see [LICENSE](LICENSE).  
Contributions: see [CONTRIBUTING.md](CONTRIBUTING.md).
