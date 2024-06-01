from abc import ABC, abstractmethod
from uuid import UUID

from .schemas import CreateRewardDTO, RewardSchema, UpdateRewardDTO, RewardResultSchema


class RewardServiceABC(ABC):

    @abstractmethod
    async def create_reward(self, reward_dto: CreateRewardDTO) -> RewardSchema:
        raise NotImplementedError

    @abstractmethod
    async def list_rewards(
        self,
        issue_id: int | None = None,
        rewarder_id: UUID | None = None
    ) -> list[RewardSchema]:
        raise NotImplementedError

    @abstractmethod
    async def update_reward(
        self,
        reward_id: UUID,
        update_fields: UpdateRewardDTO
    ) -> RewardSchema:
        raise NotImplementedError

    @abstractmethod
    async def reward_contributor(
        self,
        contributor_id: UUID,
        repo_full_name: str,
        issue_numbers: list[int]
    ) -> RewardResultSchema:
        raise NotImplementedError
