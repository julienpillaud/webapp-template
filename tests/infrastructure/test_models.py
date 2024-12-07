from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.models import Address, Post, Tag, User
from tests.fixtures.factories.factories import PostFactory, UserFactory


def test_user(session: Session, user_factory: UserFactory) -> None:
    user = user_factory.create_one()

    address_db = session.get_one(Address, user.address.id)
    assert address_db.id == user.address.id
    assert address_db.street == user.address.street
    assert address_db.city == user.address.city
    assert address_db.zip_code == user.address.zip_code
    assert address_db.country == user.address.country

    user_db = session.get_one(User, user.id)
    assert user_db.username == user.username
    assert user_db.email == user.email
    assert user_db.address == user.address
    assert user_db.posts == []


def test_post(
    session: Session, user_factory: UserFactory, post_factory: PostFactory
) -> None:
    user = user_factory.create_one()
    post = post_factory.create_one(author_id=user.id)

    user_db = session.get_one(User, user.id)
    assert user_db == user

    post_db = session.get_one(Post, post.id)
    assert post_db.title == post.title
    assert post_db.content == post.content
    assert post_db.author_id == user.id

    tags_db = session.scalars(select(Tag)).all()
    assert tags_db == post_db.tags
