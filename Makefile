.PHONY: init check test lint

init:
	uv sync --all-extras
	uv run pre-commit install

check:
	uv tree -d 1 --outdated
	uv run pre-commit autoupdate

test:
	uv run pytest

lint:
	uv run ruff format
	uv run ruff check
