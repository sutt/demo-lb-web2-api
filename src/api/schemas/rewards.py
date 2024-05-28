from pydantic import BaseModel, Field


class CreateRewardRequest(BaseModel):
    issue_html_url: str
    reward_amount: int = Field(..., gt=0)
