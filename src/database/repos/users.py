from uuid import UUID

from sqlalchemy import select

from domain.user.schemas import UserCreateDTO
from .abstract import SQLAAbstractRepo
from ..tables import UserModel


class UserRepo(SQLAAbstractRepo):

    async def create_user(self, user_dto: UserCreateDTO) -> UserModel:
        new_user = UserModel(**user_dto.dict())
        self._session.add(new_user)
        return new_user

    async def get_user_by_id(self, user_id: UUID) -> UserModel | None:
        fetched_user = await self._session.scalar(
            select(UserModel).where(UserModel.id == user_id)
        )
        return fetched_user

    async def get_user_by_github_id(self, gh_id: int) -> UserModel | None:
        fetched_user = await self._session.scalar(
            select(UserModel).where(UserModel.github_id == gh_id)
        )
        return fetched_user

    async def list(self) -> list[UserModel]:
        return await self._session.scalars(select(UserModel))

    async def add_points(self, user_id: UUID, points: int) -> UserModel:
        user = await self._session.scalar(select(UserModel).where(UserModel.id == user_id))
        user.points += points
        self._session.add(user)
        return user
