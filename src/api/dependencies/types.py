from typing import Annotated

from fastapi import Depends

from domain.user.schemas import UserSchema
from domain.user.service import UserServiceABC

from .user import get_authenticated_user


UserServiceDep = Annotated[UserServiceABC, Depends()]
GetAuthenticatedUserDep = Annotated[UserSchema, Depends(get_authenticated_user)]
