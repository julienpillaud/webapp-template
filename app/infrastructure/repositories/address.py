from typing import Never

from app.domain.models.address import AddressCreateDomain, AddressDomain
from app.infrastructure.models import Address
from app.infrastructure.repositories.base import SQLAlchemyRepositoryBase


class AddressSQLAlchemyRepository(
    SQLAlchemyRepositoryBase[
        Address,
        AddressDomain,
        AddressCreateDomain,
        Never,
    ]
):
    model = Address
    schema = AddressDomain
