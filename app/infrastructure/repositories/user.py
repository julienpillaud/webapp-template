from typing import Any

from sqlalchemy import Select
from sqlalchemy.orm import noload, selectinload

from app.domain.models.address import AddressCompactDomain
from app.domain.models.base import UserId
from app.domain.models.user import UserCreateDomain, UserDomain, UserUpdateDomain
from app.infrastructure.models import Address, User
from app.infrastructure.repositories.base import SQLAlchemyRepositoryBase
from app.infrastructure.repositories.mixin import DomainConverterMixin


class UserSQLAlchemyRepository(
    SQLAlchemyRepositoryBase[
        User,
        UserDomain,
        UserCreateDomain,
        UserUpdateDomain,
    ],
    DomainConverterMixin,
):
    model = User
    schema = UserDomain
    default_loading_options = [selectinload(User.address), noload(User.posts)]

    def _apply_loading_options(
        self, stmt: Select[tuple[User]], **kwargs: Any
    ) -> Select[tuple[User]]:
        options = [selectinload(User.address)]

        if kwargs.get("include_posts"):
            options.append(selectinload(User.posts))
        else:
            options.append(noload(User.posts))

        stmt = stmt.options(*options)
        return stmt

    def _create_model(self, data: UserCreateDomain) -> User:
        user_data = data.model_dump(exclude={"address"})
        address_data = data.address.model_dump()
        return User(**user_data, address=Address(**address_data))

    def _to_domain(self, model: User, /) -> UserDomain:
        return UserDomain(
            id=UserId(model.id),
            username=model.username,
            email=model.email,
            address=AddressCompactDomain.model_validate(model.address),
            posts=[self._convert_post_to_domain(post) for post in model.posts],
        )