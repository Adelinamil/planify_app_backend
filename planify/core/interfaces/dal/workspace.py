from typing import Protocol

from planify.core.interfaces.dal.base import Committer
from planify.core.models import dto


class WorkspaceCreator(Committer, Protocol):
    async def create(self, workspace_dto: dto.Workspace) -> dto.Workspace:
        raise NotImplementedError


class WorkspaceEditor(Committer, Protocol):
    async def update(self, workspace_dto: dto.Workspace) -> dto.Workspace:
        raise NotImplementedError


class WorkspaceRemover(Committer, Protocol):
    async def remove(self, workspace_id: int) -> None:
        raise NotImplementedError
