from sqlalchemy import delete, ScalarResult, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from planify.core.models import dto
from planify.core.utils.exceptions import ProjectMemberExists
from planify.infrastructure.db.dao.rdb.base import BaseDAO
from planify.infrastructure.db.models import ProjectMember


class ProjectMemberDAO(BaseDAO[ProjectMember]):
    def __init__(self, session: AsyncSession):
        super().__init__(ProjectMember, session)

    async def get_members(self, project_id: int) -> list[dto.ProjectMember]:
        result: ScalarResult[ProjectMember] = await self._session.scalars(
            select(ProjectMember).where(ProjectMember.project_id == project_id).options(joinedload(ProjectMember.user))
        )
        return [member.to_dto(with_user=True) for member in result.all()]

    async def create(self, project_member_dto: dto.ProjectMember) -> dto.ProjectMember:
        project_member = ProjectMember.from_dto(project_member_dto)
        self._save(project_member)
        try:
            await self._flush(project_member)
        except IntegrityError as e:
            raise ProjectMemberExists from e
        else:
            return project_member.to_dto()

    async def remove(self, project_member_dto: dto.ProjectMember):
        await self._session.execute(
            delete(ProjectMember).where(
                ProjectMember.user_id == project_member_dto.user_id,
                ProjectMember.project_id == project_member_dto.project_id,
            )
        )
