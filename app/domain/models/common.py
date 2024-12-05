from app.domain.models.base import DomainModel, UserId


class UserCompactDomain(DomainModel):
    id: UserId
    username: str
    email: str
