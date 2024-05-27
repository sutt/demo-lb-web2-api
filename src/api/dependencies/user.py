from uuid import UUID

from fastapi import FastAPI, Depends
from typing import Annotated

from domain.user.schemas import UserSchema
from domain.user.service import UserServiceABC
from impl.user import UserService

from .jwt import get_jwt_payload
from ..schemas.jwt import AccessTokenPayloadSchema


def get_service() -> UserServiceABC:
    return UserService()


def di_user(app: FastAPI):
    app.dependency_overrides[UserServiceABC] = get_service


async def get_authenticated_user(
    user_service: Annotated[UserServiceABC, Depends(get_service)],
    access_token_payload: Annotated[AccessTokenPayloadSchema, Depends(get_jwt_payload)]
) -> UserSchema:
    user_id = UUID(access_token_payload.user_id)
    return await user_service.get_by_id(user_id)
