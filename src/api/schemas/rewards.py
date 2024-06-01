from pydantic import BaseModel, Field


class CreateRewardRequest(BaseModel):
    issue_html_url: str
    reward_amount: int = Field(..., gt=0)


class CheckPullRequest(BaseModel):
    github_token: str
    repo_full_name: str
    pull_request_number: int
