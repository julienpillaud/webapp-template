from pydantic import Field

from app.domain.models.base import DomainModel, PostId, TagName, UserId


class PostDomain(DomainModel):
    id: PostId
    title: str
    content: str
    author_id: UserId
    tags: list[TagName]


class PostCreateDomain(DomainModel):
    title: str
    content: str
    author_id: UserId
    tags: list[TagName] = Field(default_factory=list)


class PostUpdateDomain(DomainModel):
    title: str | None = None
    content: str | None = None
    tags: list[TagName] | None = None
