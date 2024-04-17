from uuid import UUID

from sqlalchemy import ScalarResult, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from planify.core.models import dto
from planify.core.utils.exceptions import NoWorkspaceFound
from planify.infrastructure.db.dao.rdb.base import BaseDAO
from planify.infrastructure.db.models import Workspace, WorkspaceMember


class WorkspaceDAO(BaseDAO[Workspace]):
    def __init__(self, session: AsyncSession):
        super().__init__(Workspace, session)

    async def get_by_id(self, id_: int):
        try:
            return (await self._get_by_id(id_)).to_dto()
        except NoResultFound as e:
            raise NoWorkspaceFound from e

    async def create(self, workspace_dto: dto.Workspace) -> dto.Workspace:
        workspace = Workspace.from_dto(workspace_dto)
        self._save(workspace)
        await self._flush(workspace)
        return workspace.to_dto()

    async def update(self, workspace_dto: dto.Workspace) -> dto.Workspace:
        try:
            workspace = await self._get_by_id(workspace_dto.id)
        except NoResultFound as e:
            raise NoWorkspaceFound from e

        workspace.name = workspace_dto.name
        await self._flush(workspace)
        return workspace.to_dto()

    async def remove(self, workspace_id: int):
        await self._remove_by_id(workspace_id)

    async def get_workspaces_by_user(self, user_id: UUID) -> list[dto.Workspace]:
        result: ScalarResult[Workspace] = await self._session.scalars(
            select(Workspace).where(
                Workspace.id.in_(
                    select(WorkspaceMember.workspace_id).where(
                        WorkspaceMember.user_id == user_id, WorkspaceMember.active.is_(True)
                    )
                )
            )
        )
        return [workspace.to_dto() for workspace in result.all()]
