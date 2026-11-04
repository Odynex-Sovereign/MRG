# Changelog

All notable changes to this project are documented in this file.

## [1.1.0] — 2026-11-04

### Added
- Production application package `mrg/` with settings, structured logging, security headers
- Liveness (`/healthz`) and readiness (`/readyz`) probes plus `/info`
- Pydantic-validated WebSocket telemetry protocol with size limits
- Deterministic sandbox fallbacks for DeepSeek and sensory paths
- Multi-stage non-root Dockerfile with HEALTHCHECK and tini
- docker-compose with healthchecks, restart policy, read-only root
- GitHub Actions CI: lint, mypy, pytest, Docker build, Fly deploy on main
- Comprehensive docs: architecture, deployment, operations, runbook
- SECURITY.md, CONTRIBUTING.md, RELEASE_CHECKLIST.md, CHANGELOG.md
- Pinned dependencies and pyproject tool configuration

### Changed
- Entry point preferred as `mrg.app:app` (compat re-export kept for `services.streaming.websocket_pipeline:app`)
- WebSocket accepts both telemetry packets and `TRIGGER_CRISIS` actions
- Environment-driven configuration via `.env.example`

### Security
- Removed hardcoded production credentials from compose defaults (dev passwords only in examples)
- Non-root container user, no-new-privileges, optional trusted hosts

## [1.0.0] — prior

- Initial MRG simulation suite prototype
