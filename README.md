# MRG — Integrated Simulation Suite

**Practice composure and clear decisions when rare, high-impact events unfold.**

MRG is a consumer-ready and institution-ready simulation product for individuals, teams, schools, nonprofits, municipalities, and enterprises. It provides guided scenarios (including optional Black Swan-style challenges), a simple dashboard, transparent pricing, and a documented path to institutional licensing or perpetual buy-out.

> **One sentence:** MRG helps you train for the day the plan breaks — safely, affordably, and without claiming to predict the future.

![MRG](static/icons/logo.svg)

## Quick start (local)

```bash
git clone <this-repo>
cd MRG
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
make install
cp .env.example .env
make run
```

Open:

| URL | Purpose |
|-----|---------|
| http://localhost:8000/ | Landing page |
| http://localhost:8000/pricing | Plans |
| http://localhost:8000/demo | Live WebSocket sandbox simulation |
| http://localhost:8000/onboarding | Guided start |
| http://localhost:8000/dashboard | Application shell |
| http://localhost:8000/institutions | Licensing & buy-out |
| http://localhost:8000/healthz | Liveness |
| http://localhost:8000/readyz | Readiness |

```bash
make test
```

## What the product does

- **Landing & marketing** — clear value proposition, use cases, pricing overview, FAQ, trust notes  
- **Onboarding** — plain-language path into a free or paid plan  
- **Dashboard** — empty states, next actions, plan limits  
- **Sandbox simulations** — WebSocket-driven scenarios with labeled simulated metrics  
- **Feedback** — in-product report path  
- **Institutional materials** — proposal, SOW, security outline, deployment checklist, support options  

Capabilities that require external keys (Stripe, DeepSeek, NVIDIA) stay in **sandbox mode** until configured. The UI never pretends those integrations are live.

## Architecture

```
mrg/
  main.py           FastAPI app, routes, WebSocket
  core/
    config.py       Settings from environment
    pricing.py      Central plans & entitlements
    security.py     Headers + rate limiting
  services/
    simulation.py   Sandbox scenario engine
static/             CSS, JS, icons (design system)
templates/          Jinja2 pages
institutional/      Buy-out & procurement templates
tests/              Pytest suite
```

**Boundaries:** pricing and entitlements live only in `mrg/core/pricing.py`. Secrets only via environment / Fly secrets. Simulation outputs are explicitly labeled when simulated.

## Environment variables

See [`.env.example`](.env.example). Important:

| Variable | Purpose |
|----------|---------|
| `ENVIRONMENT` | `development` / `staging` / `production` |
| `SECRET_KEY` | Session / signing secret (required in production) |
| `PUBLIC_BASE_URL` | Canonical public URL |
| `CORS_ORIGINS` | Comma-separated origins |
| `DATABASE_URL` | Optional Postgres |
| `STRIPE_*` | Optional live billing |
| `DEEPSEEK_API_KEY` / `NVIDIA_NIM_API_KEY` | Optional model paths |
| `RATE_LIMIT_RPM` | Per-IP rate limit |

**Never commit secrets.**

## Pricing (default)

Configurable in `mrg/core/pricing.py`:

| Plan | Price | Notes |
|------|-------|-------|
| Free | $0 | 3 simulations / month |
| Personal | $5/mo or $50/yr | Black Swan + digital-twin feedback |
| Household | $10/mo or $100/yr | Up to 5 members |
| Pro | $15/mo or $150/yr | Unlimited sims, API read, custom scenarios |
| Team | $10/user/mo or $8/user/mo annual | Collaboration + audit basics |
| Nonprofit / Education | 40–60% off after verification | Eligibility workflow |
| Enterprise | Custom | SSO, dedicated, buy-out path |

Institutional buy-out **illustrative** ranges (see `/institutions` and `institutional/`):

- Small: $15,000–$40,000  
- Mid: $40,000–$125,000  
- Large: $125,000–$500,000+  

A buy-out is a **perpetual license** under contract — not an automatic IP ownership transfer unless the agreement says so.

## Docker

```bash
docker build -t mrg:local .
docker run --rm -p 8000:8000 -e SECRET_KEY=dev-only mrg:local
```

## Fly.io deployment

```bash
# Install flyctl, then:
fly launch --no-deploy   # or use existing fly.toml
fly secrets set SECRET_KEY="$(openssl rand -hex 32)"
# Optional:
# fly secrets set STRIPE_SECRET_KEY=sk_live_...
# fly secrets set DATABASE_URL=...
fly deploy
fly status
fly logs
```

Useful operations:

```bash
fly scale count 2
fly secrets list
fly releases
fly deploy --image-label rollback   # or redeploy prior release
```

Health checks hit `/healthz`. The process binds `0.0.0.0:$PORT`.

## Security model (accurate)

- Security headers and basic rate limiting enabled  
- No secrets in the repository  
- Optional billing and model keys remain inactive until set  
- We do **not** claim SOC 2, ISO 27001, or FedRAMP unless independently completed under contract  

## Accessibility

Core pages use semantic HTML, skip links, visible focus, labeled forms, and respect `prefers-reduced-motion`. See `/accessibility`.

## Testing & quality

```bash
make test
make lint
```

CI runs install, lint (advisory), and pytest on push/PR.

## Documentation map

| Doc | Content |
|-----|---------|
| `README.md` | This file |
| `institutional/*` | Proposal, SOW, security outline, checklists |
| `/security` | In-app security summary |
| `/faq` | End-user FAQ |

## License

See `LICENSE` (MIT unless otherwise noted in downstream agreements).

## Known limitations & next steps

- Full multi-tenant auth/SSO is structured for extension; default onboarding is lightweight  
- Stripe checkout activation requires operator-configured secrets  
- Persistent user data requires configuring `DATABASE_URL` and adding migrations  
- Chart-heavy operational views should continue screen-reader testing as they grow  

Recommended next steps: wire identity provider, enable Stripe webhooks for entitlements, add Postgres-backed session history, and expand E2E tests for billing once keys exist in a protected environment.
