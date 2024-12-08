import uuid
from typing import Any

from app.domain.models.base import DomainPagination, PaginationParams
from app.domain.models.user import UserCreateDomain, UserDomain, UserUpdateDomain
from app.domain.repository import AbstractRepository


class UserService:
    def __init__(
        self,
        repository: AbstractRepository[UserDomain, UserCreateDomain, UserUpdateDomain],
    ) -> None:
        self.repository = repository

    def get_all(
        self, pagination: PaginationParams | None = None, **kwargs: Any
    ) -> DomainPagination[UserDomain]:
        return self.repository.get_all(pagination=pagination, **kwargs)

    def get_by_id(self, entity_id: uuid.UUID, /, **kwargs: Any) -> UserDomain:
        return self.repository.get_by_id(entity_id, **kwargs)

    def create(self, data: UserCreateDomain) -> UserDomain:
        return self.repository.create(data)

    def update(self, entity_id: uuid.UUID, data: UserUpdateDomain, /) -> UserDomain:
        return self.repository.update(entity_id, data)

    def delete(self, entity_id: uuid.UUID, /) -> None:
        self.repository.delete(entity_id)
