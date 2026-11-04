# MRG Integrated Simulation Suite

**Planet-scale crisis simulation grid** for teams that train decision-makers under extreme cognitive and sensory pressure.

[![CI](https://github.com/Odynex-Sovereign/MRG/actions/workflows/ci.yml/badge.svg)](https://github.com/Odynex-Sovereign/MRG/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)

## Product overview

MRG combines:

- **Macro reasoning** (DeepSeek or offline sandbox)
- **WebSocket simulation channel** for live telemetry and crisis prompts
- **Sensory stream hooks** (NVIDIA Riva / Audio2Face ready)
- **Transparent SaaS pricing** with demo checkout (Stripe-ready)

**Target customers:** executive education, institutional risk teams, defense/training orgs, and operators running vertical crisis modules.

## Features

- Responsive marketing site (pricing, demo, investors, FAQ, legal templates)
- Interactive browser demo against `/ws/simulation`
- `/api/pricing` + demo checkout with validation and clear non-live labeling
- Health/readiness probes, structured logs, security headers
- Optional Postgres, Docker Compose, Fly.io, K8s manifests
- Metrics and admin demo dashboards (sample data labeled)
- Investor roadmap page with explicit placeholders

## Tech stack

| Area | Technology |
|------|------------|
| Backend | FastAPI, Uvicorn, Pydantic Settings |
| Realtime | WebSockets |
| Frontend | Accessible static HTML/CSS/JS |
| DB (optional) | PostgreSQL + asyncpg |
| Payments | Stripe adapter (demo until configured) |
| Deploy | Docker, Compose, Fly.io, Kubernetes |

See [DECISIONS.md](DECISIONS.md) for why this stack was chosen.

## Project structure

```
mrg/                 Application package (API, config, pricing, services)
app/                 Static UI pages + assets
services/            Legacy/compat modules (billing, sensory adapters)
database/            Migrations + pool helpers
deploy/              K8s + Terraform starters
docs/                Architecture, ops, runbook
tests/               Pytest suite
```

## Prerequisites

- Python 3.11+
- Optional: Docker, `flyctl`, API keys (DeepSeek, NVIDIA, Stripe)

## Local setup

```bash
git clone https://github.com/Odynex-Sovereign/MRG.git
cd MRG
python3.11 -m venv .venv
source .venv/bin/activate
make install
cp .env.example .env
make sandbox
```

Open:

- http://localhost:8000/ — home
- http://localhost:8000/pricing — plans
- http://localhost:8000/demo — live WebSocket demo
- http://localhost:8000/docs — OpenAPI (non-production)

```bash
make test
make smoke   # requires server running
```

## Environment variables

See [`.env.example`](.env.example). Important keys:

| Variable | Purpose |
|----------|---------|
| `ENVIRONMENT` | `development` / `staging` / `production` |
| `DATABASE_URL` | Optional Postgres |
| `DEEPSEEK_API_KEY` | Macro engine (sandbox if empty) |
| `NVIDIA_NIM_API_KEY` | Sensory path |
| `STRIPE_*` | Live billing (optional) |
| `ADMIN_API_TOKEN` | Protect admin summary in production |
| `CORS_ORIGINS` | Comma-separated origins |

**Never commit real secrets.**

## Pricing & subscriptions

Plans are defined in **`mrg/pricing.py`** only:

| Plan | Price |
|------|-------|
| Sandbox | $0 |
| Starter | $49/mo ($470/yr) |
| Growth | $499/mo ($4,790/yr) |
| Enterprise | Contact sales |

Checkout is **demo mode** until Stripe is connected. Full detail: [PRICING.md](PRICING.md).

## Commands

```bash
make lint format typecheck test test-cov
make sandbox docker-up docker-down migrate smoke
```

## Deployment

- Docker Compose: `make docker-up`
- Fly.io: see [DEPLOYMENT.md](DEPLOYMENT.md)
- CI: `.github/workflows/ci.yml` (lint, typecheck, test, image build, optional Fly deploy)

## Accessibility, security, SEO

- Skip links, focus styles, semantic structure, reduced-motion support
- Security headers, non-root containers, input validation
- Meta description, Open Graph, JSON-LD on home, canonical placeholders

## Troubleshooting

| Issue | Action |
|-------|--------|
| Import errors | `export PYTHONPATH=.` and reinstall requirements |
| WS fails behind proxy | Ensure WebSocket upgrade support |
| `/readyz` 503 | DB configured but unreachable — fix DSN or unset `DATABASE_URL` |
| Checkout errors | Only `free`/`starter`/`growth` are self-serve; accept terms required |

More: [docs/runbook.md](docs/runbook.md)

## Documentation index

| Doc | Purpose |
|-----|---------|
| [PRICING.md](PRICING.md) | Plans & Stripe wiring |
| [AUDIT.md](AUDIT.md) | Audit + investment scorecard |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design |
| [API.md](API.md) | HTTP/WS reference |
| [METRICS.md](METRICS.md) | Analytics events |
| [INVESTOR_READINESS.md](INVESTOR_READINESS.md) | Fundraising narrative |
| [ROADMAP.md](ROADMAP.md) | Milestones |
| [SECURITY.md](SECURITY.md) | Vulnerability reporting |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Ship checklist |
| [DECISIONS.md](DECISIONS.md) | ADRs & costs |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — [LICENSE](LICENSE).
