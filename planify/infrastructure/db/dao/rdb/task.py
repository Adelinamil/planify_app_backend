from sqlalchemy import select, Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from planify.core.models import dto
from planify.core.utils.exceptions import TaskNotFound
from planify.infrastructure.db.dao.rdb.base import BaseDAO
from planify.infrastructure.db.models import Task


class TaskDAO(BaseDAO[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)

    async def get_by_id(self, id_: int) -> dto.Task:
        try:
            return (
                await self._get_by_id(
                    id_, options=[joinedload(Task.author), joinedload(Task.performer), joinedload(Task.project)]
                )
            ).to_dto(with_author=True, with_project=True, with_performer=True)
        except NoResultFound as e:
            raise TaskNotFound from e

    async def get_by_workspace_id(self, workspace_id: int) -> list[dto.Task]:
        result = await self._session.scalars(
            select(Task)
            .where(Task.workspace_id == workspace_id)
            .order_by(Task.id.desc())
            .options(joinedload(Task.author), joinedload(Task.performer), joinedload(Task.project))
        )
        return [task.to_dto(with_author=True, with_project=True, with_performer=True) for task in result.all()]

    async def is_task_exists(self, task_id: int, workspace_id: int) -> bool:
        result: Result[tuple[Task]] = await self._session.execute(
            select(Task).where(Task.id == task_id, Task.workspace_id == workspace_id)
        )
        return bool(result.scalar())

    async def create(self, task_dto: dto.Task) -> dto.Task:
        task = Task.from_dto(task_dto)
        self._save(task)
        await self._flush(task)
        return task.to_dto()

    async def update(self, task_dto: dto.Task) -> dto.Task:
        try:
            task = await self._get_by_id(task_dto.id)
        except NoResultFound as e:
            raise TaskNotFound from e

        task.name = task_dto.name
        task.description = task_dto.description
        task.priority = task_dto.priority
        task.status = task_dto.status
        task.deadline = task_dto.deadline
        task.project_id = task_dto.project_id
        task.author_id = task_dto.author_id
        task.performer_id = task_dto.performer_id
        await self._flush(task)
        return task.to_dto()

    async def remove(self, task_id: int):
        await self._remove_by_id(task_id)
