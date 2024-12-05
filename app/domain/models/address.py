import uuid

from app.domain.models.base import AddressId, DomainModel


class AddressDomain(DomainModel):
    id: AddressId
    street: str
    city: str
    zip_code: str
    country: str
    user_id: uuid.UUID | None


class AddressCompactDomain(DomainModel):
    id: AddressId
    street: str
    city: str
    zip_code: str
    country: str


class AddressCreateDomain(DomainModel):
    street: str
    city: str
    zip_code: str
    country: str
