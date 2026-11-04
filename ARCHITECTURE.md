# Architecture

## Stack choice

| Layer | Choice | Why |
|-------|--------|-----|
| API + WS | FastAPI (Python 3.11+) | Existing core; excellent WebSocket & async support |
| UI | Static HTML/CSS/JS served by FastAPI | Fast to ship, accessible, no Node build required for MVP |
| Config | pydantic-settings | Typed env configuration |
| DB | Optional PostgreSQL + asyncpg | Stateless sandbox without DB |
| Payments | Stripe (adapter) | Industry standard subscriptions |
| Deploy | Docker, Compose, Fly.io, K8s manifests | Portable |

**Not adopted yet (documented upgrade path):** Next.js monorepo, Prisma, dedicated search, Redis queue — add when product complexity requires them (see DECISIONS.md).

## Runtime diagram

```
Browser ──HTTP──► FastAPI (pages + /api/*)
       ──WS────► /ws/simulation ──► macro service ──► DeepSeek or sandbox
                              └──► sensory service ──► mock or NVIDIA
Optional: Postgres pool, Stripe webhooks, email provider
```

## Modularity

- `mrg/pricing.py` — commercial catalog
- `mrg/services/*` — AI adapters
- `mrg/api/*` — HTTP/WS routers
- `services/billing/*` — Stripe prior art to promote when enabling billing

## Multi-tenant (foundation)

Future org model: `organizations` → `memberships` (roles) → `subscriptions`. Audit log table for sensitive actions. Not fully implemented; admin summary is demo-only.
