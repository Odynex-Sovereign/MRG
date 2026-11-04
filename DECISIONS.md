# Architecture decisions

## ADR-001: Keep FastAPI instead of rewriting to Next.js

**Decision:** Serve marketing UI as static pages from FastAPI; retain Python for simulation engine.

**Tradeoff:** Less component-driven frontend; simpler ops and one runtime for WS + API.

**Upgrade path:** Extract `app/` into a Next.js frontend that calls the same `/api` and WS endpoints when a design system team is staffed.

## ADR-002: Demo checkout before live Stripe

**Decision:** Ship honest demo checkout with clear labeling.

**Tradeoff:** No revenue automation until keys and webhooks are configured.

## ADR-003: Sample metrics

**Decision:** `/metrics` shows labeled demo data.

**Tradeoff:** Avoids fabricating traction; investors see instrumentation intent.

## Operating cost (order-of-magnitude)

- Fly.io shared VM ~$5–30/mo early stage
- Managed Postgres ~$15–50/mo
- DeepSeek/NVIDIA usage variable per session
- Stripe fees standard SaaS rates when enabled
