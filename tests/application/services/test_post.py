import uuid

import pytest
from faker import Faker
from sqlalchemy.orm import Session

from app.application.services.post import PostService
from app.domain.models.base import TagName, UserId
from app.domain.models.post import PostCreateDomain, PostUpdateDomain
from app.infrastructure.exceptions import EntityNotFoundError
from app.infrastructure.models import Post, Tag, User
from tests.fixtures.factories.factories import PostFactory, UserFactory


def test_get_posts(post_factory: PostFactory, post_service: PostService) -> None:
    count = 3
    post_factory.create_many(count)

    results = post_service.get_all()

    assert results.total == count
    assert results.limit == count
    assert len(results.items) == count


def test_get_post_by_id(post_factory: PostFactory, post_service: PostService) -> None:
    post = post_factory.create_one()

    result = post_service.get_by_id(post.id)

    assert result.id == post.id
    assert result.title == post.title
    assert result.content == post.content
    assert result.author_id == post.author_id
    assert len(result.tags) == len(post.tags)


def test_get_post_by_id_not_found(post_service: PostService) -> None:
    with pytest.raises(EntityNotFoundError):
        post_service.get_by_id(uuid.uuid4())


def test_create_post(
    faker: Faker, user_factory: UserFactory, post_service: PostService
) -> None:
    user = user_factory.create_one()
    data = PostCreateDomain(
        title=faker.sentence(),
        content=faker.text(),
        author_id=UserId(user.id),
        tags=[TagName(faker.word()) for _ in range(3)],
    )

    result = post_service.create(data)

    assert result.title == data.title
    assert result.content == data.content
    assert result.author_id == user.id
    assert len(result.tags) == len(data.tags)


def test_create_post_author_not_found(faker: Faker, post_service: PostService) -> None:
    data = PostCreateDomain(
        title=faker.sentence(),
        content=faker.text(),
        author_id=UserId(uuid.uuid4()),
        tags=[TagName(faker.word()) for _ in range(3)],
    )

    with pytest.raises(EntityNotFoundError):
        post_service.create(data)


def test_update_post(
    faker: Faker, post_factory: PostFactory, post_service: PostService
) -> None:
    post = post_factory.create_one()
    data = PostUpdateDomain(title=faker.sentence())

    result = post_service.update(post.id, data)

    assert result.title == data.title
    assert result.content == post.content
    assert result.author_id == post.author_id
    assert len(result.tags) == len(post.tags)


def test_update_post_tags(
    faker: Faker, post_factory: PostFactory, post_service: PostService
) -> None:
    post = post_factory.create_one()
    tags = [TagName(faker.word()) for _ in range(3)]
    data = PostUpdateDomain(tags=tags)

    result = post_service.update(post.id, data)

    assert set(result.tags) == set(tags)


def test_update_post_not_found(faker: Faker, post_service: PostService) -> None:
    data = PostUpdateDomain(title=faker.sentence())

    with pytest.raises(EntityNotFoundError):
        post_service.update(uuid.uuid4(), data)


def test_delete_post(
    session: Session, post_factory: PostFactory, post_service: PostService
) -> None:
    post = post_factory.create_one()

    post_service.delete(post.id)

    deleted_post = session.get(Post, post.id)
    assert deleted_post is None

    # Deleting post doesn't delete the author
    author = session.get(User, post.author_id)
    assert author is not None

    for tag in post.tags:
        session.get(Tag, tag.id)
        # TODO: handle orphan tags
        # assert deleted_tag is None


def test_delete_post_not_found(post_service: PostService) -> None:
    with pytest.raises(EntityNotFoundError):
        post_service.delete(uuid.uuid4())
