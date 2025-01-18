import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.infrastructure.models import User
from app.infrastructure.utils import SQLAlchemyInstrument
from tests.fixtures.factories.factories import PostFactory, UserFactory

number_of_users = 20
numbers_of_test_users = 10
number_of_posts = 5


@pytest.fixture
def users(user_factory: UserFactory, post_factory: PostFactory) -> list[User]:
    users = user_factory.create_many(number_of_users)
    test_users = user_factory.create_many(numbers_of_test_users, username="test")
    for user in users + test_users:
        post_factory.create_many(number_of_posts, author_id=user.id)
    return users


def test_select(
    session: Session,
    users: list[User],
    sqlalchemy_instrument: SQLAlchemyInstrument,
) -> None:
    with sqlalchemy_instrument.record():
        stmt = select(User).where(User.username == "test")
        users_db = session.scalars(stmt).all()
        assert len(users_db) == numbers_of_test_users

        for user in users_db:
            assert user.address.user_id == user.id
            assert len(user.posts) == number_of_posts

    assert sqlalchemy_instrument.queries_count == number_of_users + 1


def test_selectinload(
    session: Session,
    users: list[User],
    sqlalchemy_instrument: SQLAlchemyInstrument,
) -> None:
    with sqlalchemy_instrument.record():
        stmt = (
            select(User)
            .options(selectinload(User.address), selectinload(User.posts))
            .where(User.username == "test")
        )
        users_db = session.scalars(stmt).all()
        assert len(users_db) == numbers_of_test_users

        for user in users_db:
            assert user.address.user_id == user.id
            assert len(user.posts) == number_of_posts

    assert sqlalchemy_instrument.queries_count == 3  # noqa


def test_joinedload(
    session: Session,
    users: list[User],
    sqlalchemy_instrument: SQLAlchemyInstrument,
) -> None:
    with sqlalchemy_instrument.record():
        stmt = (
            select(User)
            .options(joinedload(User.address), joinedload(User.posts))
            .where(User.username == "test")
        )
        users_db = session.scalars(stmt).unique().all()
        assert len(users_db) == numbers_of_test_users

        for user in users_db:
            assert user.address.user_id == user.id
            assert len(user.posts) == number_of_posts

    assert sqlalchemy_instrument.queries_count == 1
