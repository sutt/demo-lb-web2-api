from uuid import UUID

from fastapi import APIRouter, status, Query, HTTPException

from domain.rewards.schemas import RewardSchema, CreateRewardDTO, RewardResultSchema

from ..dependencies.types import GetAuthenticatedUserDep, GithubServiceDep, RewardServiceDep, UserServiceDep
from ..exceptions.github import PullRequestNotFound, CouldNotFetchPullRequest, PullRequestNotMerged, \
    MergedIntoWrongBranch
from ..exceptions.http import BadRequestException
from ..schemas.exceptions import HTTPExceptionSchema
from ..schemas.rewards import CreateRewardRequest, CheckPullRequest
from ..services.github import GithubService

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
    return await reward_service.create_reward(
        CreateRewardDTO(
            rewarder_id=user.id,
            reward_amount=body.reward_amount,
            issue_github_id=issue.id,
            repo_full_name=issue.repository_full_name,
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


@router.post(
    '/check/pull-request',
    response_model=RewardResultSchema
    # TODO: Other responses
)
async def find_rewards_for_pull_request(
    body: CheckPullRequest,
    reward_service: RewardServiceDep,
    user_service: UserServiceDep
):

    gh_service = GithubService(body.github_token)

    try:
        pr = await gh_service.get_pull_request(
            repo_full_name=body.repo_full_name,
            pr_number=body.pull_request_number
        )
    except PullRequestNotFound:
        raise BadRequestException('Pull request not found.')
    except CouldNotFetchPullRequest:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='The pull request could not be fetched.'
        )

    try:
        gh_service.validate_pull_request(pr)
    except PullRequestNotMerged:
        raise BadRequestException('The pull request is not merged.')
    except MergedIntoWrongBranch:
        raise BadRequestException('The pull request has to be merged into default branch to get reward.')

    # Once we validated the PR, find all the issues that are closed by it
    issue_numbers = await gh_service.extract_issue_numbers_from_pull_request(pr)

    contributor = await user_service.get_by_github_id_or_create(pr.user.id)

    return await reward_service.reward_contributor(
        contributor_id=contributor.id,
        repo_full_name=pr.base.repo.full_name,
        issue_numbers=issue_numbers,
    )


@router.post(
    '/check/commit'
    # TODO: Response model
    # TODO: Other responses
)
async def find_rewards_for_commit(
    # TODO
):
    pass
