from typing import Protocol
from uuid import UUID

from planify.core.interfaces.dal.base import Committer
from planify.core.models import dto
from planify.core.models.enums.workspace import WorkspaceMemberRole


class WorkspaceMemberCreator(Committer, Protocol):
    async def create(self, workspace_member_dto: dto.WorkspaceMember) -> dto.WorkspaceMember:
        raise NotImplementedError


class WorkspaceMemberEditor(Committer, Protocol):
    async def update(self, workspace_member_dto: dto.WorkspaceMember) -> dto.WorkspaceMember:
        raise NotImplementedError


class IsWorkspaceMemberResolver(Protocol):
    async def is_member(
        self,
        user_id: UUID,
        workspace_id: int,
        roles: list[WorkspaceMemberRole] | None = None,
    ) -> bool:
        raise NotImplementedError
