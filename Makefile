# Makefile

.PHONY: sandbox docker-up migrate test-billing install-deps

install-deps:
	pip install -r requirements.txt

sandbox:
	PYTHONPATH=. uvicorn services.streaming.websocket_pipeline:app --reload --port 8000

docker-up:
	docker compose up -d --build

migrate:
	PYTHONPATH=. python database/db_client.py

test-billing:
	PYTHONPATH=. python tests/mock_client_test.py
