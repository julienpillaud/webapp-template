from app.domain.models.base import DomainModel, PostId, TagName
from app.domain.models.common import UserCompactDomain


class PostDomain(DomainModel):
    id: PostId
    title: str
    content: str
    author: UserCompactDomain
    tags: list[TagName]


class PostCreateDomain(DomainModel):
    title: str
    content: str


class PostUpdateDomain(DomainModel):
    title: str | None = None
    content: str | None = None
