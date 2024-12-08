from typing import Any, Generic, TypeVar

from faker import Faker
from sqlalchemy.orm import Session

from app.infrastructure.models import Address, Post, Tag, User

T = TypeVar("T")


class BaseFactory(Generic[T]):
    def __init__(self, session: Session):
        self.session = session
        self.faker = Faker()

    def create_one(self, **kwargs: Any) -> T:
        instance = self._make(**kwargs)
        self._create([instance])
        return instance

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:
        instances = [self._make(**kwargs) for _ in range(count)]
        self._create(instances)
        return instances

    def _create(self, instances: list[T]) -> None:
        self.session.add_all(instances)
        self.session.commit()

    def _make(self, **kwargs: Any) -> T:
        raise NotImplementedError


class UserFactory(BaseFactory[User]):
    def __init__(self, session: Session):
        super().__init__(session)

    def _make(self, **kwargs: Any) -> User:
        address = Address(
            street=kwargs.get("street", self.faker.street_address()),
            city=kwargs.get("city", self.faker.city()),
            zip_code=kwargs.get("zip_code", self.faker.postcode()),
            country=kwargs.get("country", self.faker.country()),
        )

        return User(
            username=kwargs.get("username", self.faker.user_name()),
            email=kwargs.get("email", self.faker.unique.email()),
            address=address,
        )


class PostFactory(BaseFactory[Post]):
    def __init__(self, session: Session, user_factory: UserFactory):
        super().__init__(session)
        self.user_factory = user_factory

    def _make(self, **kwargs: Any) -> Post:
        if not (author_id := kwargs.get("author_id")):
            author_id = self.user_factory.create_one().id

        if not (tags := kwargs.get("tags")):
            num_tags = self.faker.random_int(min=1, max=3)
            tags = [Tag(name=self.faker.unique.word()) for _ in range(num_tags)]

        return Post(
            title=kwargs.get("title", self.faker.sentence()),
            content=kwargs.get("content", self.faker.text()),
            author_id=author_id,
            tags=tags,
        )
