import uuid
from typing import Any

from app.domain.models.base import DomainPagination, PaginationParams
from app.domain.models.post import PostCreateDomain, PostDomain, PostUpdateDomain
from app.domain.repository import AbstractRepository


class PostService:
    def __init__(
        self,
        repository: AbstractRepository[PostDomain, PostCreateDomain, PostUpdateDomain],
    ) -> None:
        self.repository = repository

    def get_all(
        self, pagination: PaginationParams | None = None, **kwargs: Any
    ) -> DomainPagination[PostDomain]:
        return self.repository.get_all(pagination=pagination, **kwargs)

    def get_by_id(self, entity_id: uuid.UUID, /, **kwargs: Any) -> PostDomain:
        return self.repository.get_by_id(entity_id, **kwargs)

    def create(self, data: PostCreateDomain, /) -> PostDomain:
        return self.repository.create(data)

    def update(self, entity_id: uuid.UUID, data: PostUpdateDomain, /) -> PostDomain:
        return self.repository.update(entity_id, data)

    def delete(self, entity_id: uuid.UUID, /) -> None:
        self.repository.delete(entity_id)
