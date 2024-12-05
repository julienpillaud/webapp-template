from app.domain.models.user import UserCreateDomain, UserDomain, UserUpdateDomain
from app.infrastructure.models import User
from app.infrastructure.repositories.base import SQLAlchemyRepositoryBase


class UserSQLAlchemyRepository(
    SQLAlchemyRepositoryBase[
        User,
        UserDomain,
        UserCreateDomain,
        UserUpdateDomain,
    ]
):
    model = User
    schema = UserDomain
