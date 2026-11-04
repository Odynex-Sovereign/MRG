# MRG Integrated Simulation Suite
### Planet-Scale Crisis Simulation Grid & Autonomous Command Engine

[![License: MIT](https://shields.io)](https://opensource.org)
[![Python 3.11+](https://shields.io)](https://python.org)
[![Infrastructure: Fly.io](https://shields.io)](https://fly.io)

MRG is a highly scalable, autonomous crisis simulation grid designed to map high-stakes professional stress into live, interactive digital twins. The core application runs headless across a high-availability rolling cluster of **5 distributed server nodes**, coordinating deep textual reasoning, low-latency sensory models, out-of-band communication failovers, and multi-channel financial loops entirely hands-off.

---

## 🏗️ Technical Architecture & Core Layers
Client (Visual Dashboard / Junior Canvas) ──WebSocket (/ws/simulation)──► FastAPI Cluster (5 Nodes)
│
┌──────────────────────────────┼──────────────────────────────┬───────┴──────────────────────┐
▼                              ▼                              ▼                              ▼
Macro-Cognitive Engine       Sensory Stream Pipeline       Out-of-Band Communications     Automated Financial Router
(DeepSeek-V3 / Sandbox)      (NVIDIA Riva & Audio2Face)    (Twilio SMS / War Rooms)       (Stripe Connect & Braintree)
### 1. Visualization & Immersion Layer
* **Parallel Tensor Grids:** Vectorizes massive macro-crisis pipelines into clean matrix arrays via parallel compute pipelines, bypassing CPU blocks to execute thousands of simultaneous scenarios.
* **Multisensory Streaming:** Integrates with `NVIDIA Riva TTS` and `Audio2Face` to map live text feeds into spoken dialog and responsive digital human animations.

### 2. Autonomous Resilience Layer (`social_webhook.py`)
* **Out-of-Band Routing:** Assumes primary internal communications will crash during critical failures. Diverts telemetry triggers directly over global `Twilio SMS/Voice` nodes and external workspace hooks to safeguard lines.
* **Fleet Auto-Recovery Monitor:** Runs 24/7 background tasks (`hyper_scale.py`) that track cluster health, automatically migrating active memory states and isolating congested nodes without manual engineering input.
### 3. Comprehensive Monetization & B2B Marketplace Layer
* **Marketplace Revenue Splits:** Uses Stripe Connect to partition custom consultant scenario purchases at the edge, taking an automated 20% platform infrastructure cut completely hands-off.
* **Headless API Tokenization:** Exposes unbundled data services for enterprise developers, charging fractional usage tariffs for streaming direct data frames into third-party dashboards.
* **Dual Checkout Gateways:** Handles standard cards via Stripe and alternative digital wallets (PayPal/Venmo) via Braintree under a unified, compliant interface.
* **Contextual Upsell Loops:** Watches user stress matrices in real time and automatically pushes checkout upgrades to client chat channels right at peak tension.

---

## 📂 Vertical Market Scenario Manifest

* **`MRG_AUTO_04` (Automotive & EV Minerals):** Models multi-tier assembly lines, material markups, and unexpected supply chain blockades for raw Lithium and Cobalt.
* **`Medical Specialties Suite` (Dentistry & Plastic Surgery):** Orchestrates localized autoclave hardware disruptions alongside data extortion threats targeting sensitive client archives.
* **`Junior Academy Framework`:** A child-safe, gamified block-programming environment using custom puzzle tokens to teach younger students structural logic and agribusiness grid defense.
* **`Regional Logistics Grids`:** Targets localized infrastructure setups, including the **Texas ERCOT Power Matrix** (Bitcoin mining curtailment demand-response arbitrage) and **Southwest Georgia Agribusiness Corridors** (cold-chain preservation logistics).
---

## 🚀 Quick Start Deployment Guide

### Prerequisites
* Python 3.11+
* PostgreSQL DB Instance
* API Credentials (DeepSeek, NVIDIA NIM, Stripe, Braintree, Twilio)

### Local Configuration Setup
```bash
git clone https://github.com
cd MRG
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env # Inject appropriate platform credentials
```

### Direct Cluster Launch Sequence
```bash
# Apply database schemas
python run_migrations.py

# Initialize local sandbox playground server
uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload
```

### Production Cluster Rollout (Fly.io)
Ensure your target application environment properties match your localized cloud profile configuration secrets, then execute your deployment pipeline:
```bash
fly secrets set TWILIO_ACCOUNT_SID="AC..." BRAINTREE_ENVIRONMENT="production" STRIPE_API_KEY="sk_live_..."
flyctl deploy --config fly.toml
```

---

## 🔒 Security & Data Compliance
* **PCI-DSS Isolation:** All frontend financial checkouts use single-use tokenized nonces, deflecting card-handling vulnerabilities away from your hosting cluster.
* **COPPA / GDPR Safeguards:** Unlocks absolute privacy defaults, blocks third-party tracking, and hides user tracking on youth-focused accounts.
  
