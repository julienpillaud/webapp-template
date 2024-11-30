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
        self.session.add(instance)
        self.session.commit()
        return instance

    def create_many(self, count: int, **kwargs: Any) -> list[T]:
        instances = []
        for _ in range(count):
            instance = self._make(**kwargs)
            self.session.add(instance)
            instances.append(instance)
        self.session.commit()
        return instances

    def _make(self, **kwargs: Any) -> T:
        raise NotImplementedError


class UserFactory(BaseFactory[User]):
    def __init__(self, session: Session, address_factory: "AddressFactory"):
        super().__init__(session)
        self.address_factory = address_factory

    def _make(self, **kwargs: Any) -> User:
        address = kwargs.pop("address", self.address_factory.create_one())

        return User(
            username=kwargs.get("username", self.faker.user_name()),
            email=kwargs.get("email", self.faker.email()),
            address=address,
        )


class AddressFactory(BaseFactory[Address]):
    def _make(self, **kwargs: Any) -> Address:
        return Address(
            street=kwargs.get("street", self.faker.street_address()),
            city=kwargs.get("city", self.faker.city()),
            zip_code=kwargs.get("zip_code", self.faker.postcode()),
            country=kwargs.get("country", self.faker.country()),
        )


class PostFactory(BaseFactory[Post]):
    def __init__(self, session: Session, user_factory: UserFactory):
        super().__init__(session)
        self.user_factory = user_factory

    def _make(self, **kwargs: Any) -> Post:
        author_id = kwargs.pop("author_id", self.user_factory.create_one().id)

        tags = kwargs.pop("tags", None)
        if tags is None:
            num_tags = self.faker.random_int(min=1, max=3)
            tags = [Tag(name=self.faker.word()) for _ in range(num_tags)]

        return Post(
            title=kwargs.get("title", self.faker.sentence()),
            content=kwargs.get("content", self.faker.text()),
            author_id=author_id,
            tags=tags,
        )
