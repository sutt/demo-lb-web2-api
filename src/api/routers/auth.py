from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, status
from starlette.responses import RedirectResponse

from config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

from ..dependencies.types import UserServiceDep
from ..exceptions.github import CouldNotFetchGithubUser
from ..exceptions.http import BadRequestException
from ..schemas.exceptions import HTTPExceptionSchema
from ..schemas.jwt import TokenResponse, GetAccessTokenDTO
from ..services.github import GithubService
from ..services.jwt import JWTService

router = APIRouter(tags=['Auth'])


@router.get(
    '/github',
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def github_auth():
    params = {'client_id': GITHUB_CLIENT_ID}
    return RedirectResponse(f'https://github.com/login/oauth/authorize/?{urlencode(params)}')


@router.get(
    '/github/callback',
    response_model=TokenResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': HTTPExceptionSchema}
    }
)
async def github_callback(
    code: str,
    user_service: UserServiceDep
):  # TODO: Code validation
    async with httpx.AsyncClient() as client:
        headers = {'Accept': 'application/json'}
        body = {
            'client_id': GITHUB_CLIENT_ID,
            'client_secret': GITHUB_CLIENT_SECRET,
            'code': code,
        }
        response = await client.post(
            'https://github.com/login/oauth/access_token',
            headers=headers,
            data=body,
        )

        if response.status_code != 200:
            raise BadRequestException('Github authorization error.')

        access_token = response.json()['access_token']

        try:
            gh_user = await GithubService(access_token).get_authenticated_user()
        except CouldNotFetchGithubUser:
            raise BadRequestException('Github authorization error.')

        registered_user = await user_service.get_by_github_id_or_create(gh_user.id)

        return TokenResponse(
            access_token=JWTService.get_access_token(
                GetAccessTokenDTO(
                    user_id=registered_user.id,
                    github_token=access_token
                )
            )
        )
