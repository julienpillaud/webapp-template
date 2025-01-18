import uuid

import pytest
from faker import Faker
from sqlalchemy.orm import Session

from app.domain.models.address import AddressCreateDomain
from app.domain.models.base import PaginationParams
from app.domain.models.user import UserCreateDomain, UserUpdateDomain
from app.infrastructure.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from app.infrastructure.models import Address, Post, Tag, User
from app.infrastructure.repositories.user import UserSQLAlchemyRepository
from tests.fixtures.factories.factories import PostFactory, UserFactory


def test_get_users(
    user_factory: UserFactory, user_repository: UserSQLAlchemyRepository
) -> None:
    count = 3
    user_factory.create_many(count)

    results = user_repository.get_all()

    assert results.total == count
    assert results.limit == count
    assert len(results.items) == count


def test_get_users_first_page(
    user_factory: UserFactory, user_repository: UserSQLAlchemyRepository
) -> None:
    count = 12
    page = 1
    limit = 5
    user_factory.create_many(count)

    results = user_repository.get_all(PaginationParams(page=page, limit=limit))

    assert results.total == count
    assert results.limit == limit
    assert len(results.items) == limit


def test_get_users_last_page(
    user_factory: UserFactory, user_repository: UserSQLAlchemyRepository
) -> None:
    count = 12
    page = 3
    limit = 5
    user_factory.create_many(count)

    results = user_repository.get_all(PaginationParams(page=page, limit=limit))

    remaining = count - (limit * (page - 1))
    assert results.total == count
    assert results.limit == remaining
    assert len(results.items) == remaining


def test_get_users_empty_page(
    user_factory: UserFactory, user_repository: UserSQLAlchemyRepository
) -> None:
    count = 12
    page = 5
    limit = 5
    user_factory.create_many(count)

    results = user_repository.get_all(PaginationParams(page=page, limit=limit))

    assert results.total == count
    assert results.limit == 0
    assert len(results.items) == 0


def test_get_user_by_id(
    user_factory: UserFactory,
    post_factory: PostFactory,
    user_repository: UserSQLAlchemyRepository,
) -> None:
    number_of_posts = 3
    user = user_factory.create_one()
    post_factory.create_many(number_of_posts, author_id=user.id)

    result = user_repository.get_by_id(user.id)

    assert result.id == user.id
    assert result.username == user.username
    assert result.email == user.email
    assert result.address.id == user.address.id
    assert result.posts == []


def test_get_user_by_id_with_posts(
    user_factory: UserFactory,
    post_factory: PostFactory,
    user_repository: UserSQLAlchemyRepository,
) -> None:
    number_of_posts = 3
    user = user_factory.create_one()
    posts = post_factory.create_many(number_of_posts, author_id=user.id)

    result = user_repository.get_by_id(user.id, include_posts=True)

    assert result.id == user.id
    assert result.username == user.username
    assert result.email == user.email
    assert result.address.id == user.address.id
    assert {post.id for post in result.posts} == {post.id for post in posts}


def test_get_user_by_id_not_found(user_repository: UserSQLAlchemyRepository) -> None:
    with pytest.raises(EntityNotFoundError):
        user_repository.get_by_id(uuid.uuid4())


def test_create_user(faker: Faker, user_repository: UserSQLAlchemyRepository) -> None:
    data = UserCreateDomain(
        username=faker.user_name(),
        email=faker.email(),
        address=AddressCreateDomain(
            street=faker.street_address(),
            city=faker.city(),
            zip_code=faker.zipcode(),
            country=faker.country(),
        ),
    )

    result = user_repository.create(data)

    assert hasattr(result, "id")
    assert result.username == data.username
    assert result.email == data.email
    assert hasattr(result.address, "id")
    assert result.address.street == data.address.street
    assert result.address.city == data.address.city
    assert result.address.zip_code == data.address.zip_code
    assert result.address.country == data.address.country
    assert result.posts == []


def test_create_user_email_already_exists(
    faker: Faker, user_factory: UserFactory, user_repository: UserSQLAlchemyRepository
) -> None:
    user = user_factory.create_one()
    data = UserCreateDomain(
        username=faker.user_name(),
        email=user.email,
        address=AddressCreateDomain(
            street=faker.street_address(),
            city=faker.city(),
            zip_code=faker.zipcode(),
            country=faker.country(),
        ),
    )
    with pytest.raises(EntityAlreadyExistsError):
        user_repository.create(data)


def test_create_user_address_already_exists(
    faker: Faker, user_factory: UserFactory, user_repository: UserSQLAlchemyRepository
) -> None:
    user = user_factory.create_one()
    data = UserCreateDomain(
        username=faker.user_name(),
        email=faker.email(),
        address=AddressCreateDomain(
            street=user.address.street,
            city=user.address.city,
            zip_code=user.address.zip_code,
            country=user.address.country,
        ),
    )
    with pytest.raises(EntityAlreadyExistsError):
        user_repository.create(data)


def test_update_user(
    faker: Faker, user_factory: UserFactory, user_repository: UserSQLAlchemyRepository
) -> None:
    user = user_factory.create_one()
    data = UserUpdateDomain(username=faker.user_name())

    result = user_repository.update(user.id, data)

    assert result.username == data.username


def test_update_user_address(
    faker: Faker,
    user_factory: UserFactory,
    user_repository: UserSQLAlchemyRepository,
) -> None:
    user = user_factory.create_one()
    data = UserUpdateDomain(
        address=AddressCreateDomain(
            street=faker.street_address(),
            city=faker.city(),
            zip_code=faker.zipcode(),
            country=faker.country(),
        )
    )

    result = user_repository.update(user.id, data)

    assert data.address
    assert result.address.street == data.address.street
    assert result.address.city == data.address.city
    assert result.address.zip_code == data.address.zip_code
    assert result.address.country == data.address.country


def test_update_user_not_found(
    faker: Faker, user_repository: UserSQLAlchemyRepository
) -> None:
    data = UserUpdateDomain(username=faker.user_name())

    with pytest.raises(EntityNotFoundError):
        user_repository.update(uuid.uuid4(), data)


def test_update_user_email_already_exists(
    faker: Faker, user_factory: UserFactory, user_repository: UserSQLAlchemyRepository
) -> None:
    existing_user = user_factory.create_one()
    user_to_update = user_factory.create_one()
    data = UserUpdateDomain(email=existing_user.email)

    with pytest.raises(EntityAlreadyExistsError):
        user_repository.update(user_to_update.id, data)


def test_delete_user(
    session: Session,
    user_factory: UserFactory,
    post_factory: PostFactory,
    user_repository: UserSQLAlchemyRepository,
) -> None:
    number_of_posts = 3
    user = user_factory.create_one()
    posts = post_factory.create_many(number_of_posts, author_id=user.id)

    user_repository.delete(user.id)
    session.expunge_all()

    deleted_user = session.get(User, user.id)
    assert deleted_user is None

    address = session.get(Address, user.address.id)
    assert address is None

    for post in posts:
        deleted_post = session.get(Post, post.id)
        assert deleted_post is None

    for tag in [tag for post in posts for tag in post.tags]:
        session.get(Tag, tag.id)
        # TODO: handle orphan tags
        # assert deleted_tag is None


def test_delete_user_not_found(user_repository: UserSQLAlchemyRepository) -> None:
    with pytest.raises(EntityNotFoundError):
        user_repository.delete(uuid.uuid4())
