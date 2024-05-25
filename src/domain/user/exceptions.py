from domain.common.exceptions import DomainException


class UserException(DomainException):
    pass


class UserNotFound(UserException):
    pass
