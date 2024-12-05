import uuid
from typing import Generic, NewType, TypeVar

from pydantic import BaseModel, ConfigDict, NonNegativeInt, PositiveInt


class DomainModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


Domain_T = TypeVar("Domain_T", bound=DomainModel)
Create_T_contra = TypeVar("Create_T_contra", bound=DomainModel, contravariant=True)
Update_T_contra = TypeVar("Update_T_contra", bound=DomainModel, contravariant=True)


AddressId = NewType("AddressId", uuid.UUID)
UserId = NewType("UserId", uuid.UUID)
PostId = NewType("PostId", uuid.UUID)
TagName = NewType("TagName", str)


class PaginationParams(BaseModel):
    page: PositiveInt = 1
    limit: PositiveInt = 100


class DomainPagination(BaseModel, Generic[Domain_T]):
    total: NonNegativeInt
    limit: NonNegativeInt
    items: list[Domain_T]
