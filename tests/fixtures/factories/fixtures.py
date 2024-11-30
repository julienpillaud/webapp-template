import pytest
from sqlalchemy.orm import Session

from tests.fixtures.factories.factories import AddressFactory, PostFactory, UserFactory


@pytest.fixture
def address_factory(session: Session) -> AddressFactory:
    return AddressFactory(session=session)


@pytest.fixture
def user_factory(session: Session, address_factory: AddressFactory) -> UserFactory:
    return UserFactory(session=session, address_factory=address_factory)


@pytest.fixture
def post_factory(session: Session, user_factory: UserFactory) -> PostFactory:
    return PostFactory(session=session, user_factory=user_factory)
