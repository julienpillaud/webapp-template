from sqlalchemy.orm import selectinload

from app.domain.models.post import PostCreateDomain, PostDomain, PostUpdateDomain
from app.infrastructure.exceptions import EntityNotFoundError
from app.infrastructure.models import Post, Tag, User
from app.infrastructure.repositories.base import SQLAlchemyRepositoryBase
from app.infrastructure.repositories.mixin import DomainConverterMixin


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

    def create(self, data: PostCreateDomain, /) -> PostDomain:
        if not self.session.get(User, data.author_id):
            raise EntityNotFoundError()

        post = self.model(
            title=data.title,
            content=data.content,
            author_id=data.author_id,
            tags=[Tag(name=tag) for tag in data.tags],
        )
        self.session.add(post)
        self.session.commit()

        return self._to_domain(post)

    def _to_domain(self, model: Post, /) -> PostDomain:
        return self._convert_post_to_domain(post=model)
