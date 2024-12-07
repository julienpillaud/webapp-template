import uuid
from typing import Never

from app.core.exceptions import OperationNotAllowedError
from app.domain.models.address import AddressDomain
from app.infrastructure.models import Address
from app.infrastructure.repositories.base import SQLAlchemyRepositoryBase


class AddressSQLAlchemyRepository(
    SQLAlchemyRepositoryBase[
        Address,
        AddressDomain,
        Never,
        Never,
    ]
):
    model = Address
    schema = AddressDomain

    def create(self, data: Never, /) -> AddressDomain:
        raise OperationNotAllowedError()

    def update(self, entity_id: uuid.UUID, data: Never, /) -> AddressDomain:
        raise OperationNotAllowedError()

    def delete(self, entity_id: uuid.UUID, /) -> None:
        raise OperationNotAllowedError()
