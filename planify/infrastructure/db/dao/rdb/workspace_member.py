from typing import Sequence
from uuid import UUID

from sqlalchemy import select, Result, ScalarResult
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.interfaces import ORMOption

from planify.core.models import dto
from planify.core.models.enums.workspace import WorkspaceMemberRole
from planify.core.utils.exceptions import WorkspaceMemberExists, NoWorkspaceMemberFound, WorkspaceMemberCannotBeUpdated
from planify.infrastructure.db.dao.rdb.base import BaseDAO
from planify.infrastructure.db.models import WorkspaceMember


class WorkspaceMemberDAO(BaseDAO[WorkspaceMember]):
    def __init__(self, session: AsyncSession):
        super().__init__(WorkspaceMember, session)

    async def is_member(
        self,
        user_id: UUID,
        workspace_id: int,
        roles: list[WorkspaceMemberRole] | None = None,
    ) -> bool:
        whereclause = [
            WorkspaceMember.user_id == user_id,
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.active.is_(True),
        ]
        if roles:
            whereclause.append(WorkspaceMember.role.in_(roles))

        result: Result[tuple[WorkspaceMember]] = await self._session.execute(
            select(WorkspaceMember).where(*whereclause)
        )
        return bool(result.scalar())

    async def _get_member(
        self,
        user_id: UUID,
        workspace_id: int,
        options: Sequence[ORMOption] | None = None,
    ) -> WorkspaceMember:
        try:
            return await self._get_by_id((user_id, workspace_id), options=options)
        except NoResultFound as e:
            raise NoWorkspaceMemberFound from e

    async def get_member(self, user_id: UUID, workspace_id: int) -> dto.WorkspaceMember:
        return (
            await self._get_member(
                user_id,
                workspace_id,
                options=[joinedload(WorkspaceMember.user)],
            )
        ).to_dto(with_user=True)

    async def get_members(self, workspace_id: int) -> list[dto.WorkspaceMember]:
        result: ScalarResult[WorkspaceMember] = await self._session.scalars(
            select(WorkspaceMember)
            .where(WorkspaceMember.workspace_id == workspace_id)
            .order_by(WorkspaceMember.created_at.desc())
            .options(joinedload(WorkspaceMember.user))
        )
        return [member.to_dto(with_user=True) for member in result.all()]

    async def create(self, workspace_member_dto: dto.WorkspaceMember) -> dto.WorkspaceMember:
        workspace_member = WorkspaceMember.from_dto(workspace_member_dto)
        self._save(workspace_member)
        try:
            await self._flush(workspace_member)
        except IntegrityError as e:
            raise WorkspaceMemberExists from e
        else:
            return workspace_member.to_dto()

    async def update(self, workspace_member_dto: dto.WorkspaceMember) -> dto.WorkspaceMember:
        workspace_member = await self._get_member(workspace_member_dto.user_id, workspace_member_dto.workspace_id)
        if workspace_member.role == WorkspaceMemberRole.OWNER:
            raise WorkspaceMemberCannotBeUpdated

        workspace_member.role = workspace_member_dto.role
        workspace_member.active = workspace_member_dto.active
        await self._flush(workspace_member)
        return workspace_member.to_dto()
