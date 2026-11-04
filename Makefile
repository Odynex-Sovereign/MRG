# MRG development and deployment helpers

.PHONY: sandbox docker-up migrate test test-billing install-deps

install-deps:
	python -m pip install -r requirements.txt

sandbox:
	PYTHONPATH=. python -m uvicorn services.streaming.websocket_pipeline:app --reload --host 0.0.0.0 --port 8000

docker-up:
	docker compose up -d --build

migrate:
	PYTHONPATH=. python database/db_client.py

test:
	PYTHONPATH=. python -m pytest -q

test-billing:
	PYTHONPATH=. python tests/mock_client_test.py
