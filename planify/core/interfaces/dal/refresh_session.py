from typing import Protocol
from uuid import UUID

from .base import Committer
from ...models import dto


class RefreshSessionCreator(Committer, Protocol):
    async def count_by_user_id(self, user_id: UUID) -> int:
        raise NotImplementedError

    async def create(self, refresh_session: dto.RefreshSession) -> dto.RefreshSession:
        raise NotImplementedError

    async def remove_oldest_by_user_id(self, user_id: UUID):
        raise NotImplementedError


class RefreshSessionVerifier(Committer, Protocol):
    async def get_by_id(self, id_: UUID) -> dto.RefreshSession:
        raise NotImplementedError

    async def remove_by_id(self, id_: UUID) -> int:
        raise NotImplementedError
