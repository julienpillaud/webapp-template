import logging
from collections.abc import Iterator

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.infrastructure.models import Base

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def engine(settings: Settings) -> Iterator[Engine]:
    logger.debug(f"Creating engine {settings.SQLALCHEMY_DATABASE_URI}")
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    logger.debug("Creating database")
    Base.metadata.create_all(engine)
    yield engine
    logger.debug("Deleting database")
    Base.metadata.drop_all(engine)


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    with Session(engine) as session:
        logger.debug("Creating session")
        yield session

        session.rollback()
        logger.debug("Deleting database tables")
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
