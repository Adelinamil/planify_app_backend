from typing import Protocol
from uuid import UUID

from planify.core.interfaces.dal.base import Committer
from planify.core.models import dto


class UserCreator(Committer, Protocol):
    async def create(self, user: dto.UserWithCredentials) -> dto.User:
        raise NotImplementedError


class UserByIdResolver(Protocol):
    async def get_by_id(self, id_: UUID) -> dto.User:
        raise NotImplementedError
