from sqlalchemy import select, Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from planify.core.models import dto
from planify.core.utils.exceptions import ProjectNotFound
from planify.infrastructure.db.dao.rdb.base import BaseDAO
from planify.infrastructure.db.models import Project


class ProjectDAO(BaseDAO[Project]):
    def __init__(self, session: AsyncSession):
        super().__init__(Project, session)

    async def get_by_id(self, id_: int) -> dto.Project:
        try:
            return (
                await self._get_by_id(id_, options=[joinedload(Project.author), joinedload(Project.manager)])
            ).to_dto(with_author=True, with_manager=True)
        except NoResultFound as e:
            raise ProjectNotFound from e

    async def get_by_workspace_id(self, workspace_id: int) -> list[dto.Project]:
        result = await self._session.scalars(select(Project).where(Project.workspace_id == workspace_id))
        return [project.to_dto() for project in result.all()]

    async def is_project_exists(self, project_id: int, workspace_id: int) -> bool:
        result: Result[tuple[Project]] = await self._session.execute(
            select(Project).where(Project.id == project_id, Project.workspace_id == workspace_id)
        )
        return bool(result.scalar())

    async def create(self, project_dto: dto.Project) -> dto.Project:
        project = Project.from_dto(project_dto)
        self._save(project)
        await self._flush(project)
        return project.to_dto()

    async def update(self, project_dto: dto.Project) -> dto.Project:
        try:
            project = await self._get_by_id(project_dto.id)
        except NoResultFound as e:
            raise ProjectNotFound from e

        project.name = project.name
        project.description = project_dto.description
        project.author_id = project_dto.author_id
        project.manager_id = project_dto.manager_id
        await self._flush(project)
        return project.to_dto()

    async def remove(self, project_id: int):
        await self._remove_by_id(project_id)
