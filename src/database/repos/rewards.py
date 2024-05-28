from uuid import UUID

from sqlalchemy import select

from domain.rewards.schemas import CreateRewardDTO

from .abstract import SQLAAbstractRepo
from ..tables import RewardModel


class RewardRepo(SQLAAbstractRepo):

    async def create_reward(self, reward_dto: CreateRewardDTO) -> RewardModel:
        new_reward = RewardModel(**reward_dto.dict())
        self._session.add(new_reward)
        return new_reward

    async def list_rewards(
        self,
        issue_id: int | None = None,
        rewarder_id: UUID | None = None
    ) -> list[RewardModel]:
        stmt = select(RewardModel)
        if issue_id is not None:
            stmt = stmt.where(RewardModel.issue_github_id == issue_id)
        if rewarder_id is not None:
            stmt = stmt.where(RewardModel.rewarder_id == rewarder_id)

        return await self._session.scalars(stmt)
