import uuid

import pytest
from faker import Faker
from sqlalchemy.orm import Session

from app.domain.models.base import PaginationParams, TagName, UserId
from app.domain.models.post import PostCreateDomain, PostUpdateDomain
from app.infrastructure.exceptions import EntityNotFoundError
from app.infrastructure.models import Post, Tag, User
from app.infrastructure.repositories.post import PostSQLAlchemyRepository
from tests.fixtures.factories.factories import PostFactory, UserFactory


def test_get_posts(
    post_factory: PostFactory, post_repository: PostSQLAlchemyRepository
) -> None:
    count = 3
    post_factory.create_many(count)

    results = post_repository.get_all()

    assert results.total == count
    assert results.limit == count
    assert len(results.items) == count


def test_get_posts_first_page(
    post_factory: PostFactory, post_repository: PostSQLAlchemyRepository
) -> None:
    count = 12
    page = 1
    limit = 5
    post_factory.create_many(count)

    results = post_repository.get_all(PaginationParams(page=page, limit=limit))

    assert results.total == count
    assert results.limit == limit
    assert len(results.items) == limit


def test_get_posts_last_page(
    post_factory: PostFactory, post_repository: PostSQLAlchemyRepository
) -> None:
    count = 12
    page = 3
    limit = 5
    post_factory.create_many(count)

    results = post_repository.get_all(PaginationParams(page=page, limit=limit))

    remaining = count - (limit * (page - 1))
    assert results.total == count
    assert results.limit == remaining
    assert len(results.items) == remaining


def test_get_posts_empty_page(
    post_factory: PostFactory, post_repository: PostSQLAlchemyRepository
) -> None:
    count = 12
    page = 5
    limit = 5
    post_factory.create_many(count)

    results = post_repository.get_all(PaginationParams(page=page, limit=limit))

    assert results.total == count
    assert results.limit == 0
    assert len(results.items) == 0


def test_get_post_by_id(
    post_factory: PostFactory, post_repository: PostSQLAlchemyRepository
) -> None:
    post = post_factory.create_one()

    result = post_repository.get_by_id(post.id)

    assert result.id == post.id
    assert result.title == post.title
    assert result.content == post.content
    assert result.author_id == post.author_id
    assert len(result.tags) == len(post.tags)


def test_get_post_by_id_not_found(post_repository: PostSQLAlchemyRepository) -> None:
    with pytest.raises(EntityNotFoundError):
        post_repository.get_by_id(uuid.uuid4())


def test_create_post(
    faker: Faker, user_factory: UserFactory, post_repository: PostSQLAlchemyRepository
) -> None:
    user = user_factory.create_one()
    data = PostCreateDomain(
        title=faker.sentence(),
        content=faker.text(),
        author_id=UserId(user.id),
        tags=[TagName(faker.word()) for _ in range(3)],
    )

    result = post_repository.create(data)

    assert result.title == data.title
    assert result.content == data.content
    assert result.author_id == user.id
    assert len(result.tags) == len(data.tags)


def test_create_post_author_not_found(
    faker: Faker, post_repository: PostSQLAlchemyRepository
) -> None:
    data = PostCreateDomain(
        title=faker.sentence(),
        content=faker.text(),
        author_id=UserId(uuid.uuid4()),
        tags=[TagName(faker.word()) for _ in range(3)],
    )

    with pytest.raises(EntityNotFoundError):
        post_repository.create(data)


def test_update_post(
    faker: Faker, post_factory: PostFactory, post_repository: PostSQLAlchemyRepository
) -> None:
    post = post_factory.create_one()
    data = PostUpdateDomain(title=faker.sentence())

    result = post_repository.update(post.id, data)

    assert result.title == data.title
    assert result.content == post.content
    assert result.author_id == post.author_id
    assert len(result.tags) == len(post.tags)


def test_update_post_tags(
    faker: Faker, post_factory: PostFactory, post_repository: PostSQLAlchemyRepository
) -> None:
    post = post_factory.create_one()
    tags = [TagName(faker.word()) for _ in range(3)]
    data = PostUpdateDomain(tags=tags)

    result = post_repository.update(post.id, data)

    assert set(result.tags) == set(tags)


def test_update_post_not_found(
    faker: Faker, post_repository: PostSQLAlchemyRepository
) -> None:
    data = PostUpdateDomain(title=faker.sentence())

    with pytest.raises(EntityNotFoundError):
        post_repository.update(uuid.uuid4(), data)


def test_delete_post(
    session: Session,
    post_factory: PostFactory,
    post_repository: PostSQLAlchemyRepository,
) -> None:
    post = post_factory.create_one()

    post_repository.delete(post.id)

    deleted_post = session.get(Post, post.id)
    assert deleted_post is None

    # Deleting post doesn't delete the author
    author = session.get(User, post.author_id)
    assert author is not None

    for tag in post.tags:
        deleted_tag = session.get(Tag, tag.id)  # noqa
        # TODO: handle orphan tags
        # assert deleted_tag is None


def test_delete_post_not_found(post_repository: PostSQLAlchemyRepository) -> None:
    with pytest.raises(EntityNotFoundError):
        post_repository.delete(uuid.uuid4())
