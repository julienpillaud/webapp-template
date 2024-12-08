import uuid

from sqlalchemy.orm import Session, selectinload

from app.domain.models.post import PostCreateDomain, PostDomain, PostUpdateDomain
from app.infrastructure.models import Post, Tag
from app.infrastructure.repositories.base import SQLAlchemyRepositoryBase
from app.infrastructure.repositories.mixin import DomainConverterMixin
from app.infrastructure.repositories.user import UserSQLAlchemyRepository


class PostSQLAlchemyRepository(
    SQLAlchemyRepositoryBase[
        Post,
        PostDomain,
        PostCreateDomain,
        PostUpdateDomain,
    ],
    DomainConverterMixin,
):
    model = Post
    schema = PostDomain
    default_loading_options = [selectinload(Post.tags)]

    def __init__(self, session: Session, user_repository: UserSQLAlchemyRepository):
        super().__init__(session)
        self.user_repository = user_repository

    def create(self, data: PostCreateDomain, /) -> PostDomain:
        # Check if user exists
        self.user_repository.get_by_id(data.author_id)

        post = self.model(
            title=data.title,
            content=data.content,
            author_id=data.author_id,
            tags=[Tag(name=tag) for tag in data.tags],
        )
        self.session.add(post)

        self._commit()
        return self._to_domain(post)

    def update(self, entity_id: uuid.UUID, data: PostUpdateDomain, /) -> PostDomain:
        entity = self._get_entity_by_id(entity_id)
        entity_data = data.model_dump(exclude_unset=True)

        if "tags" in entity_data:
            entity.tags = [Tag(name=tag) for tag in entity_data.pop("tags")]

        for key, value in entity_data.items():
            setattr(entity, key, value)

        self._commit()
        return self._to_domain(entity)

    def _to_domain(self, model: Post, /) -> PostDomain:
        return self._convert_post_to_domain(post=model)
