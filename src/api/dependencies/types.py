from typing import Annotated

from fastapi import Depends

from domain.user.service import UserServiceABC


UserServiceDep = Annotated[UserServiceABC, Depends()]
