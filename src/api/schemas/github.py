from pydantic import BaseModel


class GithubUserSchema(BaseModel):
    id: int


class GithubIssueSchema(BaseModel):
    id: int
    number: int
    title: str
    html_url: str
    state: str

    repository_full_name: str
