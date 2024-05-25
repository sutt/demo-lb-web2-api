from abc import ABC, abstractmethod
from uuid import UUID

from domain.user.schemas import UserCreateDTO, UserSchema


class UserServiceABC(ABC):
    @abstractmethod
    async def create(self, user_dto: UserCreateDTO) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_by_github_id(self, gh_id: int) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_by_github_id_or_create(self, gh_id: int) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    async def list_users(self) -> list[UserSchema]:
        raise NotImplementedError
