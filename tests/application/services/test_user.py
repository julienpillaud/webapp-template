import uuid

import pytest

from app.application.services.user import UserService
from app.domain.models.user import UserUpdateDomain
from app.infrastructure.exceptions import EntityNotFoundError
from tests.fixtures.factories.factories import UserFactory


def test_get_all_users(user_factory: UserFactory, user_service: UserService) -> None:
    count = 3
    user_factory.create_many(count)

    results = user_service.get_all()

    assert results.total == count
    assert results.limit == count
    assert len(results.items) == count


def test_get_user_by_id(user_factory: UserFactory, user_service: UserService) -> None:
    user = user_factory.create_one()

    result = user_service.get_by_id(user.id)

    assert result.id == user.id
    assert result.email == user.email
    assert result.username == user.username
    assert result.address.id == user.address.id
    assert result.posts == []


def test_get_user_by_id_not_found(user_service: UserService) -> None:
    with pytest.raises(EntityNotFoundError):
        import uuid

        user_service.get_by_id(uuid.uuid4())


# @pytest.mark.xfail(reason="TO DO")
# def test_create_user(user_service: UserService) -> None:
#     data = UserCreate(
#         username="User test",
#         email="user@mail.com",
#         address=AddressCreate(
#             street="Street 1", city="City", zip_code="00000", country="France"
#         ),
#     )
#
#     result = user_service.create(data)
#
#     assert hasattr(result, "id")
#     assert result.email == data.email
#     assert result.username == data.username
# assert result.address.id == address.id


# def test_create_user_already_exists(
#     user_factory: UserFactory, user_service: UserService
# ) -> None:
#     user = user_factory.create_one()
#
#     data = UserCreate(
#         username="User test",
#         email="user@mail.com",
#         address=AddressCreate(
#             street="Street 1", city="City", zip_code="00000", country="France"
#         ),
#     )
#
#     with pytest.raises(EntityAlreadyExistsError):
#         user_service.create(data)


def test_update_user(user_factory: UserFactory, user_service: UserService) -> None:
    user = user_factory.create_one()
    data = UserUpdateDomain(username="New username")

    result = user_service.update(user.id, data)

    assert result.id == user.id
    assert result.email == user.email
    assert result.username == data.username


def test_update_user_not_found(user_service: UserService) -> None:
    data = UserUpdateDomain(username="New username")

    with pytest.raises(EntityNotFoundError):
        user_service.update(uuid.uuid4(), data)
