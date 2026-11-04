# Architecture

## Overview

MRG is a FastAPI application that exposes:

- HTTP health and metadata endpoints
- A WebSocket simulation channel that accepts client telemetry and crisis prompts, runs macro analysis, and returns structured frames (optionally with sensory metadata)

External AI providers are optional. Without API keys the system runs in **sandbox mode** with deterministic fallbacks so developers and CI can exercise the full path offline.

## Process model

```
uvicorn / gunicorn workers  →  mrg.app:create_app()
                                   │
                    lifespan: optional asyncpg pool
                                   │
                    routers: health, websocket, static UI
```

Workers are **stateless**. Durable data belongs in Postgres (or another external store). WebSocket connection state is in-memory per process; for multi-replica deployments use sticky sessions or an external pub/sub if broadcast is required.

## Request / simulation flow

1. Client opens `ws://…/ws/simulation`
2. Server sends `SYSTEM_STATUS`
3. Client sends JSON telemetry or `{ "action": "TRIGGER_CRISIS", "prompt": "…" }`
4. Server validates with Pydantic (`TelemetryPacket`)
5. `generate_macro_ripple` calls DeepSeek or sandbox logic
6. Server emits `MACRO_COGNITIVE_UPDATE`
7. Optional `SENSORY_STREAM_INFO` with mock or real audio metadata

## Configuration

All runtime configuration is loaded via `mrg.config.Settings` (pydantic-settings) from environment variables and optional `.env`.

## Extension points

| Area | Module | Notes |
|------|--------|-------|
| Macro LLM | `mrg.services.macro` | Swap provider / prompt |
| Sensory | `mrg.services.sensory` | Wire Riva gRPC / Audio2Face |
| Auth | `services/auth` | Optional API key verification |
| Billing | `services/billing` | Stripe checkout / webhooks |
| Persistence | `database/` | Migrations + pool helpers |

## NVIDIA stack

See [NVIDIA_STACK.md](../NVIDIA_STACK.md) for intended NIM / Riva / Omniverse integration targets. Those integrations are feature-flagged and safe to leave disabled.
