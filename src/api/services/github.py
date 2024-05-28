import httpx

from ..exceptions.github import CouldNotFetchGithubUser, CouldNotFetchGithubIssue, GithubIssueNotFound
from ..schemas.github import GithubUserSchema, GithubIssueSchema


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

    async def get_issue_by_html_url(self, html_url: str) -> GithubIssueSchema:
        """
        Retrieves a GitHub issue by html URL.
        :param html_url: str, example: https://github.com/octocat/Hello-World/issues/1347
        :return: GithubIssueSchema
        """

        url_components = html_url.split('/')
        if len(url_components) != 7:
            raise ValueError('Invalid url format.')

        issue_owner = url_components[3]
        issue_repo = url_components[4]
        issue_number = url_components[-1]

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'https://api.github.com/repos/{issue_owner}/{issue_repo}/issues/{issue_number}',
                headers=self._request_headers
            )

            if response.status_code == 404:
                raise GithubIssueNotFound

            if response.status_code != 200:
                raise CouldNotFetchGithubIssue

        json_response = response.json()
        return GithubIssueSchema(
            id=json_response['id'],
            number=json_response['number'],
            title=json_response['title'],
            html_url=json_response['html_url'],
            state=json_response['state'],
            repository_full_name=f'{issue_owner}/{issue_repo}'
        )
