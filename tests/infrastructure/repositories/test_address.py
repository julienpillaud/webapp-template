import pytest

from app.core.exceptions import OperationNotAllowedError
from app.infrastructure.repositories.address import AddressSQLAlchemyRepository
from tests.fixtures.factories.factories import UserFactory


def test_get_all_addresses(
    user_factory: UserFactory, address_repository: AddressSQLAlchemyRepository
) -> None:
    count = 3
    user_factory.create_many(count)

    results = address_repository.get_all()

    assert results.total == count
    assert results.limit == count
    assert len(results.items) == count


def test_get_address_by_id(
    user_factory: UserFactory, address_repository: AddressSQLAlchemyRepository
) -> None:
    user = user_factory.create_one()

    result = address_repository.get_by_id(user.address.id)

    assert result.id == user.address.id
    assert result.street == user.address.street
    assert result.city == user.address.city
    assert result.zip_code == user.address.zip_code
    assert result.city == user.address.city


def test_create_address(address_repository: AddressSQLAlchemyRepository) -> None:
    with pytest.raises(OperationNotAllowedError):
        address_repository.create(None)  # type: ignore


def test_update_address(address_repository: AddressSQLAlchemyRepository) -> None:
    with pytest.raises(OperationNotAllowedError):
        address_repository.update(None, None)  # type: ignore


def test_delete_address(address_repository: AddressSQLAlchemyRepository) -> None:
    with pytest.raises(OperationNotAllowedError):
        address_repository.delete(None)  # type: ignore
