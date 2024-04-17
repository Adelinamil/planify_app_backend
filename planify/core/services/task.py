from planify.core.interfaces.dal.project import IsProjectExistsResolver
from planify.core.interfaces.dal.task import TaskByIdResolver, TaskCreator, TaskEditor, TaskRemover
from planify.core.interfaces.dal.workspace_member import IsWorkspaceMemberResolver
from planify.core.models import dto
from planify.core.services.workspace_member import is_members
from planify.core.utils.exceptions import TaskNotFound, ProjectNotFound


async def get_task(task_id: int, workspace_id: int, dao: TaskByIdResolver) -> dto.Task:
    task = await dao.get_by_id(task_id)
    if task.workspace_id != workspace_id:
        raise TaskNotFound

    return task


async def create_task(task: dto.Task, dao: TaskCreator) -> dto.Task:
    created_task = await dao.create(task)
    await dao.commit()
    return created_task


async def edit_task(
    task: dto.Task,
    task_dao: TaskEditor,
    project_dao: IsProjectExistsResolver,
    workspace_member_dao: IsWorkspaceMemberResolver,
) -> dto.Task:
    if not await task_dao.is_task_exists(task.id, task.workspace_id):
        raise TaskNotFound

    if task.project_id is not None and not await project_dao.is_project_exists(task.project_id, task.workspace_id):
        raise ProjectNotFound

    await is_members([task.author_id, task.performer_id], task.workspace_id, workspace_member_dao)

    edited_task = await task_dao.update(task)
    await task_dao.commit()
    return edited_task


async def remove_task(task_id: int, workspace_id: int, dao: TaskRemover) -> None:
    if not await dao.is_task_exists(task_id, workspace_id):
        raise ProjectNotFound

    await dao.remove(task_id)
    await dao.commit()
    return None
