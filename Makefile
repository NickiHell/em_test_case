.PHONY: up down shell test lint migrate format check-coverage pre-commit-install security

up:
	docker compose up --build -d

down:
	docker compose down

shell:
	docker compose exec api python manage.py shell

test:
	docker compose exec api python -m pytest --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=100

lint:
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/

format:
	ruff check --fix src/ tests/
	ruff format src/ tests/

migrate:
	docker compose exec api python manage.py migrate

makemigrations:
	docker compose exec api python manage.py makemigrations

security:
	uv run bandit -r src/

check-coverage:
	docker compose exec api python -m pytest --cov=src --cov-fail-under=100 --quiet

pre-commit-install:
	pre-commit install