import re

import httpx

from ..exceptions.github import (
    CouldNotFetchGithubUser,
    CouldNotFetchGithubIssue,
    GithubIssueNotFound, PullRequestNotFound, CouldNotFetchPullRequest, PullRequestNotMerged, MergedIntoWrongBranch
)
from ..schemas.github import GithubUserSchema, GithubIssueSchema, PullRequestSchema, PullRequestBase, GithubRepoSchema, \
    GithubCommitSchema


class GithubService:

    def __init__(self, gh_token):
        self._gh_token = gh_token
        self._request_headers = {'Authorization': f'Bearer {self._gh_token}'}

    async def get_authenticated_user(self) -> GithubUserSchema:
        async with httpx.AsyncClient() as client:
            response = await client.get('https://api.github.com/user', headers=self._request_headers)

            if response.status_code != 200:
                raise CouldNotFetchGithubUser

            return GithubUserSchema(**response.json())

    async def get_issue_by_html_url(self, html_url: str) -> GithubIssueSchema:
        """
        Retrieves a GitHub issue by html URL.
        :param html_url: str. Example: https://github.com/octocat/Hello-World/issues/1347
        :return: GithubIssueSchema
        """

        url_components = html_url.split('/')
        if len(url_components) != 7:
            raise ValueError('Invalid url format.')

        repo_full_name = f'{url_components[3]}/{url_components[4]}'
        issue_number = int(url_components[-1])

        return await self.get_issue_by_repo_and_number(repo_full_name, issue_number)

    async def get_issue_by_repo_and_number(
        self,
        repo_full_name: str,
        issue_number: int
    ):
        """
        Retrieves a GitHub issue by repo and number.
        :param repo_full_name: Repository full name. Example: octocat/Hello-World
        :param issue_number: Issue number. Example: 1347
        :return: IssueSchema
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}',
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
            state_reason=json_response['state_reason'],
            repository_full_name=f'{repo_full_name}'
        )

    async def get_pull_request(
        self,
        repo_full_name: str,
        pr_number: int
    ) -> PullRequestSchema:
        async with httpx.AsyncClient() as client:
            url = f'https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}'
            params = {'state': 'closed'}

            resp = await client.get(url, headers=self._request_headers, params=params)

        if resp.status_code != 200:
            if resp.status_code == 404:
                raise PullRequestNotFound
            else:
                raise CouldNotFetchPullRequest

        return PullRequestSchema.from_api(resp.json())

    def validate_pull_request(self, pull_request: PullRequestSchema):
        if not pull_request.merged_at:
            raise PullRequestNotMerged

        if pull_request.base.ref != pull_request.base.repo.default_branch:
            raise MergedIntoWrongBranch

    async def fetch_pull_request_commits(self, pull_request: PullRequestSchema) -> list[GithubCommitSchema]:
        url = f'https://api.github.com/repos/{pull_request.base.repo.full_name}/pulls/{pull_request.number}/commits'
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self._request_headers)
            return [
                GithubCommitSchema(
                    sha=commit['sha'],
                    message=commit['commit']['message'],
                    author=GithubUserSchema(**commit['author']),
                )
                for commit in resp.json()
            ]

    def _find_issue_numbers(self, text: str) -> list[int]:
        # Define the regex pattern to match linked issues
        pattern = r'(close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)\s+#(\d+)'

        # Find all matches in the commit message
        matches = re.findall(pattern, text, re.IGNORECASE)

        # Extract issue numbers from the matches
        linked_issues = set([int(match[1]) for match in matches])

        return list(linked_issues)

    async def extract_issue_numbers_from_pull_request(
        self,
        pr: PullRequestSchema
    ) -> list[int]:
        issue_numbers: list[int] = []
        issue_numbers.extend(self._find_issue_numbers(pr.body))
        commits = await self.fetch_pull_request_commits(pr)
        for commit in commits:
            issue_numbers.extend(self._find_issue_numbers(commit.message))

        return list(set(issue_numbers))
