from app.core.exceptions import RepositoryError


class EntityNotFoundError(RepositoryError): ...


class EntityAlreadyExistsError(RepositoryError): ...
