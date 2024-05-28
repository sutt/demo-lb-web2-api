from typing import Annotated

from fastapi import Depends

from ..schemas.jwt import AccessTokenPayloadSchema
from ..services.github import GithubService

from .jwt import get_jwt_payload


def get_github_service(
    access_token: Annotated[AccessTokenPayloadSchema, Depends(get_jwt_payload)]
) -> GithubService:
    return GithubService(access_token.github_token)
