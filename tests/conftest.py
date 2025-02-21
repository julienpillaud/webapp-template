import logging

import pytest

from app.core.config import Settings

logger = logging.getLogger(__name__)

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.repositories",
    "tests.fixtures.services",
    "tests.fixtures.factories.fixtures",
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    env_file = "tests/.env.test"
    logger.info(f"Load settings from {env_file}")
    return Settings(_env_file=env_file)  # type: ignore
