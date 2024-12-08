import pytest
from sqlalchemy.orm import Session

from app.infrastructure.repositories.address import AddressSQLAlchemyRepository
from app.infrastructure.repositories.post import PostSQLAlchemyRepository
from app.infrastructure.repositories.user import UserSQLAlchemyRepository


@pytest.fixture
def address_repository(session: Session) -> AddressSQLAlchemyRepository:
    return AddressSQLAlchemyRepository(session=session)


@pytest.fixture
def user_repository(session: Session) -> UserSQLAlchemyRepository:
    return UserSQLAlchemyRepository(session=session)


@pytest.fixture
def post_repository(
    session: Session, user_repository: UserSQLAlchemyRepository
) -> PostSQLAlchemyRepository:
    return PostSQLAlchemyRepository(session=session, user_repository=user_repository)
