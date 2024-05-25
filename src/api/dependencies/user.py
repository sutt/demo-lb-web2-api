from fastapi import FastAPI

from domain.user.service import UserServiceABC
from impl.user import UserService


def get_service() -> UserServiceABC:
    return UserService()


def di_user(app: FastAPI):
    app.dependency_overrides[UserServiceABC] = get_service
