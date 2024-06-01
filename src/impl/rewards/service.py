from datetime import datetime
from uuid import UUID

from database.repos import UserRepo
from database.repos.rewards import RewardRepo
from database.session import SessionScope
from database.tables import RewardModel
from domain.rewards.schemas import CreateRewardDTO, RewardSchema, UpdateRewardDTO, RewardResultSchema
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

    async def reward_contributor(
        self,
        contributor_id: UUID,  # Should be already registered
        repo_full_name: str,
        issue_numbers: list[int]
    ) -> RewardResultSchema:
        rewarded_for: list[RewardModel] = []
        already_claimed: list[RewardModel] = []

        async with SessionScope.get_session() as session:
            existing_rewards = await RewardRepo(session).list_rewards(
                repo_full_name=repo_full_name,
                issue_numbers=issue_numbers
            )

            claimed_at = datetime.utcnow()
            total_points = 0
            for reward in existing_rewards:
                if reward.winner_id is None:  # Reward the contributor
                    reward.winner_id = contributor_id
                    reward.claimed_at = claimed_at
                    total_points += reward.reward_amount
                    rewarded_for.append(reward)
                    session.add(reward)
                else:  # This issue has been already solved
                    already_claimed.append(reward)

            if len(rewarded_for):
                await UserRepo(session).add_points(contributor_id, total_points)
                await session.commit()

        rewarded_for_schemas = []
        for reward in rewarded_for:
            await session.refresh(reward)
            rewarded_for_schemas.append(
                RewardSchema.model_validate(reward)
            )

        return RewardResultSchema(
            total_points=total_points,
            rewarded_for=rewarded_for_schemas,
            already_claimed=[
                RewardSchema.model_validate(reward)
                for reward in already_claimed
            ]
        )

