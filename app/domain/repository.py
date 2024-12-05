import uuid
from typing import Any, Protocol

from app.domain.models.base import (
    Create_T_contra,
    Domain_T,
    DomainPagination,
    PaginationParams,
    Update_T_contra,
)


class AbstractRepository(Protocol[Domain_T, Create_T_contra, Update_T_contra]):
    schema: type[Domain_T]

    def get_all(
        self, pagination: PaginationParams | None = None, **kwargs: Any
    ) -> DomainPagination[Domain_T]: ...

    def get_by_id(self, entity_id: uuid.UUID, /, **kwargs: Any) -> Domain_T: ...

    def create(self, data: Create_T_contra, /) -> Domain_T: ...

    def update(self, entity_id: uuid.UUID, data: Update_T_contra, /) -> Domain_T: ...

    def delete(self, entity_id: uuid.UUID, /) -> None: ...
