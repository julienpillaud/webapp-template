import logging
from typing import Any

import pytest
from pytest import FixtureRequest, Item, Parser
from sqlalchemy import Engine, event

from app.core.config import Settings
from app.infrastructure.utils import after_cursor_execute, before_cursor_execute

logger = logging.getLogger(__name__)

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.repositories",
    "tests.fixtures.services",
    "tests.fixtures.factories.fixtures",
]


def pytest_addoption(parser: Parser) -> None:
    parser.addoption("--db", action="store_true", default=False)


@pytest.fixture(scope="session")
def log_level(request: FixtureRequest) -> Any:
    return request.config.getoption("log_cli_level")


def pytest_runtest_call(item: Item) -> None:
    level = item.session.config.getoption("log_cli_level")
    if level == "debug":
        event.listen(Engine, "before_cursor_execute", before_cursor_execute)
        event.listen(Engine, "after_cursor_execute", after_cursor_execute)


def pytest_runtest_teardown(item: Item) -> None:
    level = item.session.config.getoption("log_cli_level")
    if level == "debug":
        event.remove(Engine, "before_cursor_execute", before_cursor_execute)
        event.remove(Engine, "after_cursor_execute", after_cursor_execute)


@pytest.fixture(scope="session")
def settings() -> Settings:
    env_file = "tests/.env.test"
    logger.info(f"Load settings from {env_file}")
    return Settings(_env_file=env_file)  # type: ignore
