import logging
from collections.abc import Iterator

import pytest
from _pytest.fixtures import FixtureRequest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.infrastructure.models import Base
from app.infrastructure.utils import SQLAlchemyInstrument

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def engine(settings: Settings) -> Engine:
    logger.info(f"Create engine {settings.SQLALCHEMY_DATABASE_URI}")
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    logger.info("Drop all tables")
    Base.metadata.drop_all(engine)
    logger.info("Create all tables")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(request: FixtureRequest, engine: Engine) -> Iterator[Session]:
    with Session(engine, expire_on_commit=False) as session:
        logger.debug("Creating session")
        yield session

        if not request.config.getoption("--db"):
            session.rollback()
            logger.debug("Deleting database tables")
            for table in reversed(Base.metadata.sorted_tables):
                session.execute(table.delete())
            session.commit()


@pytest.fixture(scope="session")
def sqlalchemy_instrument(engine: Engine) -> SQLAlchemyInstrument:
    return SQLAlchemyInstrument(engine)
