import uuid

from sqlalchemy import Column, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)


post_tag = Table(
    "post_tag",
    Base.metadata,
    Column("post_id", ForeignKey("post.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)


class Address(Base):
    street: Mapped[str]
    city: Mapped[str]
    zip_code: Mapped[str]
    country: Mapped[str]

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )

    __table_args__ = (UniqueConstraint("street", "city", "zip_code", "country"),)


class User(Base):
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)

    address: Mapped[Address] = relationship(cascade="all, delete-orphan")
    posts: Mapped[list["Post"]] = relationship(cascade="all, delete-orphan")


class Post(Base):
    title: Mapped[str]
    content: Mapped[str]
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )

    tags: Mapped[list["Tag"]] = relationship(secondary=post_tag)


class Tag(Base):
    name: Mapped[str] = mapped_column(unique=True)
