import logging

import pytest
from _pytest.config.argparsing import Parser
from sqlalchemy import Engine, event

from app.core.config import Settings
from app.infrastructure.utils import log_sql_statement

logger = logging.getLogger(__name__)

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.repositories",
    "tests.fixtures.services",
    "tests.fixtures.factories.fixtures",
]


def pytest_addoption(parser: Parser) -> None:
    parser.addoption("--db", action="store_true", default=False)


def pytest_sessionstart() -> None:
    event.listen(Engine, "before_cursor_execute", log_sql_statement)


@pytest.fixture(scope="session")
def settings() -> Settings:
    env_file = "tests/.env.test"
    logger.info(f"Load settings from {env_file}")
    return Settings(_env_file=env_file)  # type: ignore
