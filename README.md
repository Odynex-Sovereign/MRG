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

## Production (Fly.io)

See original deployment blueprint or:

```bash
fly launch --no-deploy
fly secrets set NVIDIA_NIM_API_KEY=... DEEPSEEK_API_KEY=... DATABASE_URL=...
fly deploy
```

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

## What Was Fixed / Added in this Package

- Complete `requirements.txt` (previously missing → Docker would fail)
- Critical syntax error in WebSocket pipeline (code outside function scope)
- Indentation / import errors in billing and legacy shim
- Sequential, complete PostgreSQL migrations (base tables created first)
- Correct NVIDIA NIM & DeepSeek API endpoints (OpenAI-compatible)
- Graceful sandbox fallbacks when API keys are absent
- Health checks, CORS, lifespan DB pool
- `.env.example`, `Makefile`, improved Dockerfiles
- NVIDIA stack documentation
- Frontend `JSON.stringify` fix

---

## License

MIT — see `LICENSE`.

## Security / Compliance Notes

See `SECURITY.md` and `TERMS.md`. Prior-art registry supports TUTSA-style defensive publication tracking.
