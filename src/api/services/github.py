import httpx

from api.exceptions.github import CouldNotFetchGithubUser
from api.schemas.github import GithubUserSchema


class GithubService:

    def __init__(self, gh_token):
        self._gh_token = gh_token
        self._request_headers = {'Authorization': f'Bearer {self._gh_token}'}

    async def get_authenticated_user(self) -> GithubUserSchema:
        async with httpx.AsyncClient() as client:
            response = await client.get('https://api.github.com/user', headers=self._request_headers)

            if response.status_code != 200:
                raise CouldNotFetchGithubUser

            return GithubUserSchema(id=response.json()['id'])
