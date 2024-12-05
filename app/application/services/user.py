import uuid
from typing import Any

from app.application.dtos import UserCreate
from app.application.services.address import AddressService
from app.domain.models.base import DomainPagination, PaginationParams
from app.domain.models.user import UserCreateDomain, UserDomain, UserUpdateDomain
from app.domain.repository import AbstractRepository
from app.infrastructure.exceptions import EntityNotFoundError


class UserService:
    def __init__(
        self,
        repository: AbstractRepository[UserDomain, UserCreateDomain, UserUpdateDomain],
        address_service: AddressService,
    ) -> None:
        self.repository = repository
        self.address_service = address_service

    def get_all(
        self, pagination: PaginationParams | None = None, **kwargs: Any
    ) -> DomainPagination[UserDomain]:
        return self.repository.get_all(pagination=pagination, **kwargs)

    def get_by_id(self, entity_id: uuid.UUID, /, **kwargs: Any) -> UserDomain:
        return self.repository.get_by_id(entity_id, **kwargs)

    def create(self, data: UserCreate) -> UserDomain:
        address = self.address_service.get_by_id(data.address_id)
        if not address:
            raise EntityNotFoundError()
        user_data = UserCreateDomain(username=data.username, email=data.email)
        return self.repository.create(user_data)

    def update(self, entity_id: uuid.UUID, data: UserUpdateDomain, /) -> UserDomain:
        return self.repository.update(entity_id, data)

    def delete(self, entity_id: uuid.UUID, /) -> None:
        self.repository.delete(entity_id)
