# MRG development helpers

.PHONY: install lint format test run clean

install:
	python -m pip install -U pip
	python -m pip install -r requirements.txt
	python -m pip install -e .[dev]

run:
	PYTHONPATH=. python -m uvicorn mrg.main:app --host 0.0.0.0 --port 8000

lint:
	python -m ruff check .

format:
	python -m black .

test:
	PYTHONPATH=. python -m pytest -q

clean:
	rm -rf .venv __pycache__ .pytest_cache
