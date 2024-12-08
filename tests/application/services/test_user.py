import uuid

import pytest
from faker import Faker

from app.application.services.user import UserService
from app.domain.models.address import AddressCreateDomain
from app.domain.models.user import UserCreateDomain, UserUpdateDomain
from app.infrastructure.exceptions import EntityNotFoundError
from tests.fixtures.factories.factories import PostFactory, UserFactory


def test_get_users(user_factory: UserFactory, user_service: UserService) -> None:
    count = 3
    user_factory.create_many(count)

    results = user_service.get_all()

    assert results.total == count
    assert results.limit == count
    assert len(results.items) == count


def test_get_user_by_id(
    user_factory: UserFactory, post_factory: PostFactory, user_service: UserService
) -> None:
    number_of_posts = 3
    user = user_factory.create_one()
    post_factory.create_many(number_of_posts, author_id=user.id)

    result = user_service.get_by_id(user.id)

    assert result.id == user.id
    assert result.email == user.email
    assert result.username == user.username
    assert result.address.id == user.address.id
    assert result.posts == []


def test_get_user_by_id_with_posts(
    user_factory: UserFactory,
    post_factory: PostFactory,
    user_service: UserService,
) -> None:
    number_of_posts = 3
    user = user_factory.create_one()
    posts = post_factory.create_many(number_of_posts, author_id=user.id)

    result = user_service.get_by_id(user.id, include_posts=True)

    assert result.id == user.id
    assert result.username == user.username
    assert result.email == user.email
    assert result.address.id == user.address.id
    assert {post.id for post in result.posts} == {post.id for post in posts}


def test_get_user_by_id_not_found(user_service: UserService) -> None:
    with pytest.raises(EntityNotFoundError):
        import uuid

        user_service.get_by_id(uuid.uuid4())


def test_create_user(faker: Faker, user_service: UserService) -> None:
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

    result = user_service.create(data)

    assert hasattr(result, "id")
    assert result.username == data.username
    assert result.email == data.email
    assert hasattr(result.address, "id")
    assert result.address.street == data.address.street
    assert result.address.city == data.address.city
    assert result.address.zip_code == data.address.zip_code
    assert result.address.country == data.address.country
    assert result.posts == []


def test_update_user(
    faker: Faker, user_factory: UserFactory, user_service: UserService
) -> None:
    user = user_factory.create_one()
    data = UserUpdateDomain(username=faker.user_name())

    result = user_service.update(user.id, data)

    assert result.username == data.username


def test_update_user_not_found(faker: Faker, user_service: UserService) -> None:
    data = UserUpdateDomain(username=faker.user_name())

    with pytest.raises(EntityNotFoundError):
        user_service.update(uuid.uuid4(), data)
