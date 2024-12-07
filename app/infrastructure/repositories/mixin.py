from app.domain.models.base import PostId, TagName, UserId
from app.domain.models.post import PostDomain
from app.infrastructure.models import Post


class DomainConverterMixin:
    @staticmethod
    def _convert_post_to_domain(post: Post) -> PostDomain:
        return PostDomain(
            id=PostId(post.id),
            title=post.title,
            content=post.content,
            author_id=UserId(post.author_id),
            tags=[TagName(tag.name) for tag in post.tags],
        )
