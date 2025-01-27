import uuid
from typing import Any, ClassVar, Generic, TypeVar

from psycopg.errors import UniqueViolation
from sqlalchemy import Select, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.interfaces import LoaderOption

from app.core.exceptions import RepositoryError
from app.domain.models.base import (
    Create_T_contra,
    Domain_T,
    DomainPagination,
    PaginationParams,
    Update_T_contra,
)
from app.domain.repository import AbstractRepository
from app.infrastructure.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from app.infrastructure.models import Base

Model_T = TypeVar("Model_T", bound=Base)


class SQLAlchemyRepositoryBase(
    AbstractRepository[Domain_T, Create_T_contra, Update_T_contra],
    Generic[
        Model_T,
        Domain_T,
        Create_T_contra,
        Update_T_contra,
    ],
):
    model: type[Model_T]
    default_loading_options: ClassVar[list[LoaderOption]] = []

    def __init__(self, session: Session):
        self.session = session

    def get_all(
        self, pagination: PaginationParams | None = None, **kwargs: Any
    ) -> DomainPagination[Domain_T]:
        count_stmt = select(func.count()).select_from(self.model)
        total = self.session.scalar(count_stmt) or 0

        stmt = select(self.model)
        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)
        stmt = self._apply_loading_options(stmt=stmt, **kwargs)

        results = self.session.scalars(stmt)
        items = [self._to_domain(result) for result in results]

        return DomainPagination(total=total, limit=len(items), items=items)

    def get_by_id(self, entity_id: uuid.UUID, /, **kwargs: Any) -> Domain_T:
        entity = self._get_entity_by_id(entity_id, **kwargs)
        return self._to_domain(entity)

    def create(self, data: Create_T_contra, /) -> Domain_T:
        db_model = self._create_model(data=data)
        self.session.add(db_model)
        self._commit()
        return self._to_domain(db_model)

    def update(self, entity_id: uuid.UUID, data: Update_T_contra, /) -> Domain_T:
        entity = self._get_entity_by_id(entity_id)

        entity_data = data.model_dump(exclude_unset=True)
        for key, value in entity_data.items():
            setattr(entity, key, value)

        self._commit()
        return self._to_domain(entity)

    def delete(self, entity_id: uuid.UUID, /) -> None:
        entity = self._get_entity_by_id(entity_id)
        self.session.delete(entity)
        self.session.commit()

    def _get_entity_by_id(self, entity_id: uuid.UUID, /, **kwargs: Any) -> Model_T:
        stmt = select(self.model).where(self.model.id == entity_id)
        stmt = self._apply_loading_options(stmt=stmt, **kwargs)
        if entity := self.session.scalar(stmt):
            return entity

        raise EntityNotFoundError()

    def _to_domain(self, model: Model_T, /) -> Domain_T:
        return self.schema.model_validate(model)

    def _apply_loading_options(
        self, stmt: Select[tuple[Model_T]], **kwargs: Any
    ) -> Select[tuple[Model_T]]:
        if self.default_loading_options:
            stmt = stmt.options(*self.default_loading_options)
        return stmt

    @staticmethod
    def _apply_pagination(
        stmt: Select[tuple[Model_T]], pagination: PaginationParams | None
    ) -> Select[tuple[Model_T]]:
        if pagination is None:
            return stmt

        offset = (pagination.page - 1) * pagination.limit
        return stmt.offset(offset).limit(pagination.limit)

    def _create_model(self, data: Create_T_contra) -> Model_T:
        return self.model(**data.model_dump())

    def _commit(self) -> None:
        try:
            self.session.commit()
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                raise EntityAlreadyExistsError() from err
            raise RepositoryError() from err
