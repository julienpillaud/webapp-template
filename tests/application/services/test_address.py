import uuid

import pytest

from app.application.services.address import AddressService
from app.domain.models.address import AddressCreateDomain
from app.infrastructure.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from tests.fixtures.factories.factories import AddressFactory


def test_get_all_addresses(
    address_factory: AddressFactory, address_service: AddressService
) -> None:
    count = 3
    address_factory.create_many(count)

    results = address_service.get_all()

    assert results.total == count
    assert results.limit == count
    assert len(results.items) == count


def test_get_address_by_id(
    address_factory: AddressFactory, address_service: AddressService
) -> None:
    address = address_factory.create_one()

    result = address_service.get_by_id(address.id)

    assert result.id == address.id
    assert result.street == address.street
    assert result.city == address.city
    assert result.zip_code == address.zip_code
    assert result.country == address.country
    assert result.user_id == address.user_id


def test_get_address_by_id_not_found(
    address_factory: AddressFactory, address_service: AddressService
) -> None:
    with pytest.raises(EntityNotFoundError):
        address_service.get_by_id(uuid.uuid4())


def test_create_address(address_service: AddressService) -> None:
    address_create = AddressCreateDomain(
        street="Street 1",
        city="City 1",
        zip_code="00000",
        country="FR",
    )

    address = address_service.create(address_create)

    assert hasattr(address, "id")
    assert address.street == address_create.street
    assert address.city == address_create.city
    assert address.zip_code == address_create.zip_code
    assert address.country == address_create.country
    assert address.user_id is None


def test_create_address_already_exists(
    address_factory: AddressFactory, address_service: AddressService
) -> None:
    address = address_factory.create_one()
    address_create = AddressCreateDomain(
        street=address.street,
        city=address.city,
        zip_code=address.zip_code,
        country=address.country,
    )

    with pytest.raises(EntityAlreadyExistsError):
        address_service.create(address_create)
