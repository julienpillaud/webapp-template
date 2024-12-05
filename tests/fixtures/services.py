import pytest

from app.application.services.address import AddressService
from app.application.services.user import UserService
from app.infrastructure.repositories.address import AddressSQLAlchemyRepository
from app.infrastructure.repositories.user import UserSQLAlchemyRepository


@pytest.fixture
def address_service(address_repository: AddressSQLAlchemyRepository) -> AddressService:
    return AddressService(repository=address_repository)


@pytest.fixture
def user_service(
    user_repository: UserSQLAlchemyRepository, address_service: AddressService
) -> UserService:
    return UserService(repository=user_repository, address_service=address_service)
