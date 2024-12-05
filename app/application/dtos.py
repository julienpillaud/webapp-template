from pydantic import BaseModel

from app.domain.models.base import AddressId


class UserCreate(BaseModel):
    username: str
    email: str
    address_id: AddressId
