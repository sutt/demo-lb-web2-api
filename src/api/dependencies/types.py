from typing import Annotated

from fastapi import Depends

from domain.rewards.service import RewardServiceABC
from domain.user.schemas import UserSchema
from domain.user.service import UserServiceABC
from .user import get_authenticated_user

from ..services.github import GithubService
from .github import get_github_service

GithubServiceDep = Annotated[GithubService, Depends(get_github_service)]

UserServiceDep = Annotated[UserServiceABC, Depends()]
GetAuthenticatedUserDep = Annotated[UserSchema, Depends(get_authenticated_user)]

RewardServiceDep = Annotated[RewardServiceABC, Depends()]
