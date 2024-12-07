import uuid
from typing import Any, Never

from app.domain.models.address import (
    AddressDomain,
)
from app.domain.models.base import DomainPagination, PaginationParams
from app.domain.repository import AbstractRepository


class AddressService:
    def __init__(
        self,
        repository: AbstractRepository[AddressDomain, Never, Never],
    ) -> None:
        self.repository = repository

    def get_all(
        self, pagination: PaginationParams | None = None, **kwargs: Any
    ) -> DomainPagination[AddressDomain]:
        return self.repository.get_all(pagination=pagination, **kwargs)

    def get_by_id(self, entity_id: uuid.UUID, /, **kwargs: Any) -> AddressDomain:
        return self.repository.get_by_id(entity_id, **kwargs)
