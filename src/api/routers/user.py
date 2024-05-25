from uuid import UUID

from fastapi import APIRouter, status, Query

from domain.user.exceptions import UserNotFound
from domain.user.schemas import UserSchema, UserCreateDTO

from ..dependencies.types import UserServiceDep
from ..exceptions.http import BadRequestException, NotFoundException
from ..schemas.exceptions import HTTPExceptionSchema


router = APIRouter(tags=['User'])


# Temporary route for testing purposes
@router.post(
    '/{gh_id}',
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchema
)
async def create_user(gh_id: int, user_service: UserServiceDep):
    return await user_service.create(UserCreateDTO(github_id=gh_id))


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=UserSchema | list[UserSchema],
    responses={
        status.HTTP_404_NOT_FOUND: {'model': HTTPExceptionSchema},
        status.HTTP_400_BAD_REQUEST: {'model': HTTPExceptionSchema}
    }
)
async def get_user(
    user_service: UserServiceDep,
    user_id: UUID | None = Query(None),
    github_id: int | None = Query(None)
):
    if not any([user_id, github_id]):
        return await user_service.list_users()

    try:
        if user_id:
            return await user_service.get_by_id(user_id)
        else:
            return await user_service.get_by_github_id(github_id)
    except UserNotFound:
        raise NotFoundException('User not found.')
