# Audit report — MRG

## Issues found (prior state)

- Fragmented Python modules at repo root with broken/fragile imports
- WebSocket protocol mismatched mock client vs server (`action` requirement)
- Unpinned dependencies; minimal tests
- Hardcoded database passwords in compose examples
- Deploy-only CI without quality gates
- Static UI limited to basic pricing cards; incomplete product surface
- No centralized public pricing API; catalog buried in config scripts
- No investor, metrics, admin, onboarding, or legal templates
- Checkout not present; payment claims unclear
- Accessibility and SEO minimal (no skip links, weak metadata)

## Fixes applied

- Production `mrg/` package with settings, logging, security headers, health/ready probes
- Validated WebSocket telemetry + crisis protocol with size limits
- Pinned deps, ruff/mypy/pytest, GitHub Actions CI
- Multi-stage non-root Docker, compose healthchecks
- **Centralized pricing** in `mrg/pricing.py` + `/api/pricing` and demo checkout
- Multi-page responsive UI: home, pricing, checkout, demo, onboarding, investors, metrics, admin, FAQ, status, legal
- Analytics event hooks (`mrgTrack`) with documented event names
- Investor/roadmap page with **explicit placeholder** labels
- Metrics dashboard with **DEMO DATA** label
- Documentation suite (see below)
- Security headers, policy templates, no secrets in tree

## Remaining limitations

- Stripe not live — demo checkout only
- Admin/metrics use sample data (no DB-backed multi-tenant admin yet)
- Auth/SSO and org workspaces are architectural stubs
- HTML/CSS multi-page (not Next.js SPA) — intentional to avoid stack bloat
- Policy pages are templates, not legal advice
- Docker not executed in the build environment used for this ZIP (CLI absent); CI defines the build path

## Assumptions

- Placeholder public prices: Free $0, Starter $49/mo, Growth $499/mo, Enterprise custom
- Enterprise module rates retained from historical `billing_catalog.py` as indicative only
- Canonical URL host `https://example.com` is a placeholder for SEO tags
- FastAPI retained as primary backend (WebSocket-native, already production-hardened in v1.1)

## Investment readiness scorecard

| Dimension | Score (1–5) | Notes |
|-----------|-------------|-------|
| Product | 4 | Clear value prop, demo, pricing, onboarding |
| Technology | 4 | Modular FastAPI, WS, Docker, CI |
| Security | 3 | Headers, non-root, templates; SOC2 still future |
| Scalability | 3 | Stateless app; DB/Stripe path documented |
| Monetization | 4 | Transparent plans + demo checkout + Stripe guide |
| Documentation | 5 | Full diligence pack |
| Go-to-market | 3 | Landing + pricing + contact; no CRM integration |

**Implemented vs future:** live Stripe, SSO, multi-tenant RBAC, real analytics warehouse, and counsel-approved policies remain recommended next steps (see ROADMAP.md).
