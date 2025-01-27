import contextlib
import logging
import time
from collections.abc import Iterator

import docker
import psycopg
import pytest
from docker.errors import NotFound
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.infrastructure.models import Base
from app.infrastructure.utils import SQLAlchemyInstrument

logger = logging.getLogger(__name__)


def wait_for_database_ready(dsn: str, timeout: int = 10) -> None:
    start_time = time.time()

    while True:
        try:
            logger.info("Waiting for database to be ready...")
            conn = psycopg.connect(dsn)
            conn.close()
            break
        except psycopg.OperationalError:
            logger.debug("Database not ready")

        if time.time() - start_time > timeout:
            raise TimeoutError

        time.sleep(1)


@pytest.fixture(scope="session")
def engine(settings: Settings) -> Engine:
    logger.info(f"Create engine {settings.SQLALCHEMY_DATABASE_URI}")
    return create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


@pytest.fixture(scope="session")
def setup_db(settings: Settings, engine: Engine) -> Iterator[None]:
    container_name = "postgres"
    client = docker.from_env()

    with contextlib.suppress(NotFound):
        existing_container = client.containers.get(container_name)
        existing_container.stop()
        existing_container.remove()

    container = client.containers.run(
        "postgres:latest",
        name="postgres",
        environment={
            "POSTGRES_USER": settings.POSTGRES_USER,
            "POSTGRES_PASSWORD": settings.POSTGRES_PASSWORD,
            "POSTGRES_DB": settings.POSTGRES_DB,
        },
        ports={"5432/tcp": settings.POSTGRES_PORT},
        detach=True,
    )
    wait_for_database_ready(dsn=settings.PSYCOPG_DSN)
    logger.info("Postgres database ready")

    logger.info("Drop all tables")
    Base.metadata.drop_all(engine)
    logger.info("Create all tables")
    Base.metadata.create_all(engine)

    yield

    container.stop()
    container.remove()


@pytest.fixture
def session(setup_db: Iterator[None], engine: Engine) -> Iterator[Session]:
    with Session(engine, expire_on_commit=False) as session:
        logger.debug("Creating session")
        yield session

        session.rollback()
        logger.debug("Deleting database tables")
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()


@pytest.fixture(scope="session")
def sqlalchemy_instrument(engine: Engine) -> SQLAlchemyInstrument:
    return SQLAlchemyInstrument(engine)
