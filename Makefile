PYTHON ?= python3
VENV ?= .venv
APP_MODULE := services.streaming.websocket_pipeline:app
PORT ?= 8000

.PHONY: venv install sandbox docker-up migrate test

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	. $(VENV)/bin/activate && pip install -U pip && pip install -r requirements.txt

sandbox: install
	. $(VENV)/bin/activate && PYTHONPATH=. uvicorn $(APP_MODULE) --host 0.0.0.0 --port $(PORT) --reload

docker-up:
	docker compose up --build -d

migrate:
	DATABASE_URL=$${DATABASE_URL:-postgresql://mrg_admin:mrg_secure_password_2026@localhost:5432/mrg_simulation_grid} python run_migrations.py

test: install
	. $(VENV)/bin/activate && pytest -q
