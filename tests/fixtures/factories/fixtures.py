import pytest
from faker import Faker
from sqlalchemy.orm import Session

from tests.fixtures.factories.factories import PostFactory, UserFactory


@pytest.fixture
def faker() -> Faker:
    return Faker()


@pytest.fixture
def user_factory(session: Session) -> UserFactory:
    return UserFactory(session=session)


@pytest.fixture
def post_factory(session: Session, user_factory: UserFactory) -> PostFactory:
    return PostFactory(session=session, user_factory=user_factory)
