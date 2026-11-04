# Changelog

## [1.2.0] — 2026-11-04

### Added
- Centralized public pricing catalog (`mrg/pricing.py`) and `/api/pricing`
- Demo checkout API and `/checkout` UI (explicitly non-live)
- Multi-page product site: pricing, demo, onboarding, investors, metrics, admin, FAQ, status, legal
- Contact API and form; analytics event hooks (`mrgTrack`)
- PRICING.md, AUDIT.md, ARCHITECTURE.md, API.md, METRICS.md, INVESTOR_READINESS.md, ROADMAP.md, DEPLOYMENT.md, DECISIONS.md
- Pricing/checkout/metrics API tests
- Admin summary endpoint with optional token gate

### Changed
- Version 1.2.0; README rewritten for product + engineering onboarding
- App factory serves static pages and mounts `/assets`

### Security
- Additional security headers (`Permissions-Policy`)
- Demo data clearly labeled; no fabricated live payment claims

## [1.1.0] — 2026-11-04

- Production `mrg/` package, health/ready probes, Docker/CI hardening, sandbox AI fallbacks

## [1.0.0] — prior

- Initial prototype suite
