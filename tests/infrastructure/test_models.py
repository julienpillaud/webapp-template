from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.models import User


def test_user(session: Session) -> None:
    user = User(
        username="test",
        email="test@example.com",
    )
    session.add(user)
    session.commit()

    stmt = select(User).where(User.email == user.email)
    result = session.scalars(stmt).one()
    assert result.username == user.username
    assert result.email == user.email
