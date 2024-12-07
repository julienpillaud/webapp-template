import uuid

import pytest

from app.application.services.address import AddressService
from app.infrastructure.exceptions import EntityNotFoundError
from tests.fixtures.factories.factories import UserFactory


def test_get_all_addresses(
    user_factory: UserFactory, address_service: AddressService
) -> None:
    count = 3
    user_factory.create_many(count)

    results = address_service.get_all()

    assert results.total == count
    assert results.limit == count
    assert len(results.items) == count


def test_get_address_by_id(
    user_factory: UserFactory, address_service: AddressService
) -> None:
    user = user_factory.create_one()

    result = address_service.get_by_id(user.address.id)

    assert result.id == user.address.id
    assert result.street == user.address.street
    assert result.city == user.address.city
    assert result.zip_code == user.address.zip_code
    assert result.country == user.address.country
    assert result.user_id == user.id


def test_get_address_by_id_not_found(address_service: AddressService) -> None:
    with pytest.raises(EntityNotFoundError):
        address_service.get_by_id(uuid.uuid4())
