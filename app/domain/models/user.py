from app.domain.models.address import AddressCompactDomain, AddressCreateDomain
from app.domain.models.base import DomainModel, UserId
from app.domain.models.post import PostDomain


class UserDomain(DomainModel):
    id: UserId
    username: str
    email: str
    address: AddressCompactDomain
    posts: list[PostDomain]


class UserCreateDomain(DomainModel):
    username: str
    email: str
    address: AddressCreateDomain


class UserUpdateDomain(DomainModel):
    username: str | None = None
    email: str | None = None
    address: AddressCreateDomain | None = None
