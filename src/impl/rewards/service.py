from uuid import UUID

from database.repos.rewards import RewardRepo
from database.session import SessionScope
from domain.rewards.schemas import CreateRewardDTO, RewardSchema, UpdateRewardDTO
from domain.rewards.service import RewardServiceABC


class RewardService(RewardServiceABC):

    async def create_reward(self, reward_dto: CreateRewardDTO) -> RewardSchema:
        async with SessionScope.get_session() as session:
            new_reward = await RewardRepo(session).create_reward(reward_dto)
            await session.commit()
            return RewardSchema.model_validate(new_reward)

    async def list_rewards(
        self,
        issue_id: int | None = None,
        rewarder_id: UUID | None = None
    ) -> list[RewardSchema]:
        async with SessionScope.get_session() as session:
            return [
                RewardSchema.model_validate(fetched_reward)
                for fetched_reward in await RewardRepo(session).list_rewards(issue_id, rewarder_id)
            ]

    async def update_reward(
        self,
        reward_id: UUID,
        update_fields: UpdateRewardDTO
    ) -> RewardSchema:
        # TODO
        pass
