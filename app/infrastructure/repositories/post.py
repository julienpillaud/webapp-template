from app.domain.models.post import PostCreateDomain, PostDomain, PostUpdateDomain
from app.infrastructure.models import Post
from app.infrastructure.repositories.base import SQLAlchemyRepositoryBase


class PostSQLAlchemyRepository(
    SQLAlchemyRepositoryBase[
        Post,
        PostDomain,
        PostCreateDomain,
        PostUpdateDomain,
    ]
):
    model = Post
    schema = PostDomain
