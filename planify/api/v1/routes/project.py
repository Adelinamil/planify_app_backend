from typing import Annotated

from fastapi import APIRouter, Depends

from planify.api.dependencies import current_user
from planify.api.dependencies.workspace import check_workspace
from planify.api.v1.models.validation.project import CreateProjectModel, EditProjectModel
from planify.core.models import dto
from planify.core.models.enums.workspace import WorkspaceMemberRole
from planify.core.services import project as services
from planify.core.utils.exceptions import NoWorkspaceFound
from planify.infrastructure.db.dao.holder import HolderDAO
from planify.infrastructure.di.db import dao_provider


async def get_project(
    project_id: int,
    workspace_id: Annotated[int, Depends(check_workspace())],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> dto.Project:
    return await services.get_project(project_id, workspace_id, dao.project)


async def get_projects(
    workspace_id: Annotated[int, Depends(check_workspace())],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> list[dto.Project]:
    return await dao.project.get_by_workspace_id(workspace_id)


async def create_project(
    create_project_model: CreateProjectModel,
    workspace_id: int,
    user: Annotated[dto.User, Depends(current_user)],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> dto.Project:
    if not await dao.workspace_member.is_member(
        user_id=user.id,
        workspace_id=workspace_id,
        roles=[WorkspaceMemberRole.ADMIN, WorkspaceMemberRole.OWNER],
    ):
        raise NoWorkspaceFound

    return await services.create_project(create_project_model.to_dto(user.id, workspace_id), dao.project)


async def edit_project(
    project_id: int,
    edit_project_model: EditProjectModel,
    workspace_id: Annotated[
        int, Depends(check_workspace(roles=[WorkspaceMemberRole.ADMIN, WorkspaceMemberRole.OWNER]))
    ],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> dto.Project:
    return await services.edit_project(
        project=edit_project_model.to_dto(project_id, workspace_id),
        project_dao=dao.project,
        workspace_member_dao=dao.workspace_member,
    )


async def remove_project(
    project_id: int,
    workspace_id: Annotated[
        int, Depends(check_workspace(roles=[WorkspaceMemberRole.ADMIN, WorkspaceMemberRole.OWNER]))
    ],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> None:
    return await services.remove_project(project_id, workspace_id, dao.project)


def setup() -> APIRouter:
    router = APIRouter(prefix="/projects", tags=["projects"])
    router.add_api_route("", get_projects, methods=["GET"])
    router.add_api_route("", create_project, methods=["POST"])
    router.add_api_route("/{project_id}", get_project, methods=["GET"])
    router.add_api_route("/{project_id}", edit_project, methods=["PUT"])
    router.add_api_route("/{project_id}", remove_project, methods=["DELETE"])
    return router
