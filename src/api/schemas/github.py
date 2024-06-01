from typing import Any

from pydantic import BaseModel, Field


class GithubUserSchema(BaseModel):
    id: int
    login: str


class GithubIssueSchema(BaseModel):
    id: int
    number: int
    title: str
    html_url: str
    state: str
    state_reason: str | None = Field(None)

    repository_full_name: str


class GithubRepoSchema(BaseModel):
    id: int
    full_name: str
    default_branch: str


class PullRequestBase(BaseModel):
    ref: str
    repo: GithubRepoSchema


class PullRequestSchema(BaseModel):
    id: int
    number: int
    title: str
    body: str = Field('')
    merged_at: str | None = Field(None)
    state: str
    user: GithubUserSchema
    base: PullRequestBase

    @staticmethod
    def from_api(obj: Any) -> 'PullRequestSchema':
        pr_user = GithubUserSchema(**obj['user'])
        pr_repo = GithubRepoSchema(**obj['base']['repo'])
        pr_base = PullRequestBase(ref=obj['base']['ref'], repo=pr_repo)

        return PullRequestSchema(
            id=obj['id'],
            number=obj['number'],
            title=obj['title'],
            body=obj['body'],
            merged_at=obj['merged_at'],
            state=obj['state'],
            user=pr_user,
            base=pr_base
        )


class GithubCommitSchema(BaseModel):
    sha: str
    message: str
    author: GithubUserSchema
