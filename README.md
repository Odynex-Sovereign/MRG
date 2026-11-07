# MRG — Integrated Simulation Suite

**Practice composure and clear decisions when rare, high-impact events unfold.**

MRG is a consumer-ready and institution-ready simulation product for individuals, teams, schools, nonprofits, municipalities, and enterprises.  
It provides guided scenarios (including optional Black Swan-style challenges), a simple dashboard, transparent pricing, and a documented path to institutional licensing or perpetual buy-out.

> **One sentence:** MRG helps you train for the day the plan breaks — safely, affordably, and without claiming to predict the future.

## Quick start (local)

```bash
# Clone / extract
cd MRG-main   # or your preferred directory name

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install
make install
# or: pip install -r requirements.txt && pip install -e .[dev]

# Configure
cp .env.example .env
# Edit .env — never commit real secrets

# Run
make run
# or: PYTHONPATH=. uvicorn mrg.main:app --host 0.0.0.0 --port 8000 --reload
