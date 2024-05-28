from uuid import UUID

from fastapi import APIRouter, status, Query

from domain.rewards.schemas import RewardSchema, CreateRewardDTO

from ..dependencies.types import GetAuthenticatedUserDep, GithubServiceDep, RewardServiceDep
from ..schemas.exceptions import HTTPExceptionSchema
from ..schemas.rewards import CreateRewardRequest


router = APIRouter(tags=['Rewards'])


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=RewardSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {'model': HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {'model': HTTPExceptionSchema},
    }
)
async def assign_reward(
    user: GetAuthenticatedUserDep,
    gh_service: GithubServiceDep,
    reward_service: RewardServiceDep,
    body: CreateRewardRequest
):
    issue = await gh_service.get_issue_by_html_url(body.issue_html_url)
    owner, repo = issue.repository_full_name.split('/')
    return await reward_service.create_reward(
        CreateRewardDTO(
            rewarder_id=user.id,
            reward_amount=body.reward_amount,
            issue_github_id=issue.id,
            issue_github_owner=owner,
            issue_github_repo=repo,
            issue_github_number=issue.number,
            html_url=issue.html_url,
        )
    )


@router.get(
    '/',
    response_model=list[RewardSchema],
)
async def list_rewards(
    reward_service: RewardServiceDep,
    issue_id: int | None = Query(None),
    rewarder_id: UUID | None = Query(None)
):
    return await reward_service.list_rewards(issue_id, rewarder_id)
