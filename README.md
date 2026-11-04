# MRG Integrated Simulation Suite: Planet-Scale Crisis Arena 🌐🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![NVIDIA Stack](https://img.shields.io/badge/NVIDIA-NIM%20%7C%20Riva%20%7C%20Audio2Face%20%7C%20Omniverse-76B900)](docs/NVIDIA_STACK.md)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)

MRG is a distributed, planet-scale crisis simulation grid. It combines long-horizon global structural reasoning (DeepSeek-V3) with hyper-low-latency micro-conversational avatars (NVIDIA Nemotron / NIM) and sensory engines (Riva + Audio2Face) to stress-test executive composure under extreme pressure.

---

## Quick Start (Sandbox — no keys required)

```bash
# 1. Clone / extract
cd MRG

# 2. Create virtualenv & install
python3.11 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Run the core engine
make sandbox
# or: PYTHONPATH=. uvicorn services.streaming.websocket_pipeline:app --reload --port 8000
```

Open http://localhost:8000/docs and http://localhost:8000/healthz

### WebSocket smoke test
```bash
python tests/mock_client_test.py
```

---

## Full Local Stack (Postgres + Engine)

```bash
cp .env.example .env
# (optional) fill NVIDIA_NIM_API_KEY / DEEPSEEK_API_KEY

make docker-up
# wait ~15 s for health
make migrate
python tests/mock_client_test.py
```

---

## Production (Fly.io) – recommended

```bash
# 1. From the fixed package root
fly launch --no-deploy --name mrg   # or pick a free name

# 2. Set secrets (DATABASE_URL optional for pure sandbox)
fly secrets set NVIDIA_NIM_API_KEY=nvapi-... DEEPSEEK_API_KEY=sk-... 
# optional:
# fly secrets set DATABASE_URL=postgresql://user:pass@host:5432/mrg

# 3. Deploy
fly deploy

# 4. Verify
fly status
fly logs
curl https://<your-app>.fly.dev/healthz
```

The process now stays running after boot. Health checks pass immediately; WebSocket endpoint is at `/ws/simulation`.

---

## Architecture Summary

| Tier | Technology | Purpose |
|------|------------|---------|
| Macro-Cognitive | DeepSeek-V3 / Llama-3-405B | Systemic ripple / market butterfly effects |
| Micro-Cognitive | NVIDIA Nemotron-4 NIM | Sub-50 ms adversarial dialogue |
| Sensory | NVIDIA Riva + Audio2Face | Vocal stress + blendshape streaming |
| Rendering | NVIDIA Omniverse + OpenUSD + Livepeer | Pixel-streamed digital twins |
| Persistence | PostgreSQL 15 | Session telemetry, seats, prior-art registry |

Full NVIDIA integration notes: **[docs/NVIDIA_STACK.md](docs/NVIDIA_STACK.md)**

---

## Verticals Supported

Corporate · Political/Media · Healthcare · Veterinary · Industrial · Military/Tactical · Aviation · Cyber Defense · Geopolitical · Central Banking Macro · Sovereign Logistics · Higher-Ed

---

## What Was Fixed / Added in this Package (Fly.io stable boot)

- Complete, installable `requirements.txt` (fastapi, uvicorn[standard], sqlalchemy, psycopg2-binary, asyncpg, python-dotenv, …)
- Top-level `sqlalchemy` import no longer crashes the process when the package is missing or slow to load
- Guarded / optional imports for db_client, deepseek_client, riva_tts → full sandbox mode without any API keys
- Added `generate_macro_ripple()` compatibility helper + correct DeepSeek API base URL
- `get_db()` dependency that never blocks boot (returns None on connection failure)
- Hardened Dockerfile with HEALTHCHECK and proxy-headers
- fly.toml: `auto_stop_machines = "off"`, explicit health check on `/healthz`, min_machines_running = 1, proper env
- dotenv made optional so Fly secrets work without a local .env
- Graceful fallbacks everywhere so the process stays alive after “booting”

---

## License

MIT — see `LICENSE`.

## Security / Compliance Notes

See `SECURITY.md` and `TERMS.md`. Prior-art registry supports TUTSA-style defensive publication tracking.
