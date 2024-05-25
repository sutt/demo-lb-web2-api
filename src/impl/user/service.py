from uuid import UUID

from database.repos import UserRepo
from database.session import SessionScope
from domain.user.exceptions import UserNotFound
from domain.user.schemas import UserCreateDTO, UserSchema
from domain.user.service import UserServiceABC


class UserService(UserServiceABC):

    async def create(self, user_dto: UserCreateDTO) -> UserSchema:
        async with SessionScope.get_session() as session:
            user_repo = UserRepo(session)
            new_user = await user_repo.create_user(user_dto)
            await session.commit()
            return UserSchema.model_validate(new_user)

    async def get_by_id(self, user_id: UUID) -> UserSchema:
        async with SessionScope.get_session() as session:
            user_repo = UserRepo(session)
            fetched_user = await user_repo.get_user_by_id(user_id)
            if not fetched_user:
                raise UserNotFound
            return UserSchema.model_validate(fetched_user)

    async def get_by_github_id(self, gh_id: int) -> UserSchema:
        async with SessionScope.get_session() as session:
            user_repo = UserRepo(session)
            fetched_user = await user_repo.get_user_by_github_id(gh_id)
            if not fetched_user:
                raise UserNotFound
            return UserSchema.model_validate(fetched_user)

    async def get_by_github_id_or_create(self, gh_id: int) -> UserSchema:
        async with SessionScope.get_session() as session:
            user_repo = UserRepo(session)
            fetched_user = await user_repo.get_user_by_github_id(gh_id)
            if not fetched_user:
                fetched_user = await user_repo.create_user(UserCreateDTO(github_id=gh_id))
                await session.commit()
            return UserSchema.model_validate(fetched_user)

    async def list_users(self) -> list[UserSchema]:
        async with SessionScope.get_session() as session:
            return [
                UserSchema.model_validate(fetched_user)
                for fetched_user in await UserRepo(session).list()
            ]
