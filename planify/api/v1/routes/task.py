from typing import Annotated

from fastapi import APIRouter, Depends

from planify.api.dependencies import current_user
from planify.api.dependencies.workspace import check_workspace
from planify.api.v1.models.validation.task import CreateTaskModel, EditTaskModel
from planify.core.models import dto
from planify.core.models.enums.workspace import WorkspaceMemberRole
from planify.core.services import task as services
from planify.core.utils.exceptions import NoWorkspaceFound
from planify.infrastructure.db.dao.holder import HolderDAO
from planify.infrastructure.di.db import dao_provider


async def get_task(
    task_id: int,
    workspace_id: Annotated[int, Depends(check_workspace())],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> dto.Task:
    return await services.get_task(task_id, workspace_id, dao.task)


async def get_tasks(
    workspace_id: Annotated[int, Depends(check_workspace())],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> list[dto.Task]:
    return await dao.task.get_by_workspace_id(workspace_id)


async def create_task(
    create_task_model: CreateTaskModel,
    workspace_id: int,
    user: Annotated[dto.User, Depends(current_user)],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> dto.Task:
    if not await dao.workspace_member.is_member(
        user_id=user.id,
        workspace_id=workspace_id,
        roles=[WorkspaceMemberRole.EDITOR, WorkspaceMemberRole.ADMIN, WorkspaceMemberRole.OWNER],
    ):
        raise NoWorkspaceFound

    return await services.create_task(create_task_model.to_dto(user.id, workspace_id), dao.task)


async def edit_task(
    task_id: int,
    edit_task_model: EditTaskModel,
    workspace_id: Annotated[
        int,
        Depends(
            check_workspace(
                roles=[
                    WorkspaceMemberRole.EDITOR,
                    WorkspaceMemberRole.ADMIN,
                    WorkspaceMemberRole.OWNER,
                ]
            )
        ),
    ],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> dto.Task:
    return await services.edit_task(
        task=edit_task_model.to_dto(task_id, workspace_id),
        task_dao=dao.task,
        project_dao=dao.project,
        workspace_member_dao=dao.workspace_member,
    )


async def remove_task(
    task_id: int,
    workspace_id: Annotated[
        int,
        Depends(
            check_workspace(
                roles=[
                    WorkspaceMemberRole.ADMIN,
                    WorkspaceMemberRole.OWNER,
                ]
            )
        ),
    ],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> None:
    return await services.remove_task(task_id, workspace_id, dao.task)


def setup() -> APIRouter:
    router = APIRouter(prefix="/tasks", tags=["tasks"])
    router.add_api_route("", get_tasks, methods=["GET"])
    router.add_api_route("", create_task, methods=["POST"])
    router.add_api_route("/{task_id}", get_task, methods=["GET"])
    router.add_api_route("/{task_id}", edit_task, methods=["PUT"])
    router.add_api_route("/{task_id}", remove_task, methods=["DELETE"])
    return router
