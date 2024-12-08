.PHONY: help init check docker-up docker-down test cov lint

include tests/.env.test
export

help:
	@echo "Available targets:"
	@echo "  init    - Set up dependencies and pre-commit hooks."
	@echo "  check   - Check outdated dependencies and update hooks."
	@echo "  test    - Run tests with pytest."
	@echo "  cov     - Run tests and generate coverage reports"
	@echo "  lint    - Format and check code with ruff and mypy."


init:
	uv sync --all-extras
	uv run pre-commit install

check:
	uv tree -d 1 --outdated
	uv run pre-commit autoupdate

docker-up:
	docker compose up -d postgres
	@until docker compose exec postgres pg_isready; \
	do \
		echo "Waiting for postgres..."; \
		sleep 1; \
	done

docker-down:
	docker compose down

test:
	uv run pytest

cov:
	uv run coverage run --source=app -m pytest
	uv run coverage report --show-missing
	uv run coverage html

lint:
	uv run ruff format
	uv run ruff check --fix
	uv run mypy .
