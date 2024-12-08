from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.infrastructure.models import User
from tests.fixtures.factories.factories import UserFactory


def test_count(session: Session, user_factory: UserFactory) -> None:
    number = 10
    user_factory.create_many(number)

    count_stmt = select(func.count()).select_from(User)
    total = session.scalar(count_stmt)

    assert total == number
