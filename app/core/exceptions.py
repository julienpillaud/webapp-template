class ApplicationError(Exception): ...


class RepositoryError(ApplicationError): ...


class OperationNotAllowedError(ApplicationError): ...
