from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from planify.api.dependencies.auth import current_user
from planify.api.dependencies.workspace import check_workspace
from planify.api.v1.models.response.workspace import WorkspaceMemberResponseModel
from planify.api.v1.models.validation.workspace import (
    CreateWorkspaceModel,
    AddMemberModel,
    EditWorkspaceModel,
    EditMemberModel,
)
from planify.core.models import dto
from planify.core.models.enums.workspace import WorkspaceMemberRole
from planify.core.services import workspace as services
from planify.infrastructure.db.dao.holder import HolderDAO
from planify.infrastructure.di.db import dao_provider


async def get_workspace(
    workspace_id: Annotated[int, Depends(check_workspace())],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> dto.Workspace:
    return await dao.workspace.get_by_id(workspace_id)


async def get_workspaces(
    user: Annotated[dto.User, Depends(current_user)],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> list[dto.Workspace]:
    return await dao.workspace.get_workspaces_by_user(user.id)


async def create_workspace(
    workspace: CreateWorkspaceModel,
    user: Annotated[dto.User, Depends(current_user)],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> dto.Workspace:
    return await services.create_workspace(
        user_id=user.id,
        workspace=workspace.to_dto(),
        workspace_dao=dao.workspace,
        workspace_member_dao=dao.workspace_member,
    )


async def edit_workspace(
    workspace_id: Annotated[int, Depends(check_workspace(roles=[WorkspaceMemberRole.OWNER]))],
    edit_workspace_model: EditWorkspaceModel,
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> dto.Workspace:
    return await services.edit_workspace(
        workspace=edit_workspace_model.to_dto(workspace_id),
        workspace_dao=dao.workspace,
    )


async def remove_workspace(
    workspace_id: Annotated[int, Depends(check_workspace(roles=[WorkspaceMemberRole.OWNER]))],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> None:
    return await services.remove_workspace(workspace_id=workspace_id, workspace_dao=dao.workspace)


async def get_workspace_member(
    workspace_id: Annotated[int, Depends(check_workspace())],
    user_id: UUID,
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> WorkspaceMemberResponseModel:
    return WorkspaceMemberResponseModel.from_dto(
        await dao.workspace_member.get_member(user_id=user_id, workspace_id=workspace_id)
    )


async def get_workspace_members(
    workspace_id: Annotated[int, Depends(check_workspace())],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> list[WorkspaceMemberResponseModel]:
    return [
        WorkspaceMemberResponseModel.from_dto(member_dto)
        for member_dto in await dao.workspace_member.get_members(workspace_id=workspace_id)
    ]


async def add_workspace_member(
    workspace_id: Annotated[
        int, Depends(check_workspace(roles=[WorkspaceMemberRole.ADMIN, WorkspaceMemberRole.OWNER]))
    ],
    add_member_model: AddMemberModel,
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> dto.WorkspaceMember:
    return await services.add_workspace_member(
        workspace_member=add_member_model.to_dto(workspace_id),
        user_dao=dao.user,
        workspace_member_dao=dao.workspace_member,
    )


async def edit_workspace_member(
    workspace_id: Annotated[
        int, Depends(check_workspace(roles=[WorkspaceMemberRole.ADMIN, WorkspaceMemberRole.OWNER]))
    ],
    edit_member_model: EditMemberModel,
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> dto.WorkspaceMember:
    return await services.edit_workspace_member(
        workspace_member=edit_member_model.to_dto(workspace_id),
        workspace_member_dao=dao.workspace_member,
    )


def setup() -> APIRouter:
    router = APIRouter(prefix="/workspaces", tags=["workspaces"])

    # workspaces
    router.add_api_route("", get_workspaces, methods=["GET"])
    router.add_api_route("", create_workspace, methods=["POST"])
    router.add_api_route("/{workspace_id}", get_workspace, methods=["GET"])
    router.add_api_route("/{workspace_id}", edit_workspace, methods=["PUT"])
    router.add_api_route("/{workspace_id}", remove_workspace, methods=["DELETE"])

    # members
    router.add_api_route("/{workspace_id}/members", get_workspace_members, methods=["GET"])
    router.add_api_route("/{workspace_id}/members", add_workspace_member, methods=["POST"])
    router.add_api_route("/{workspace_id}/members", edit_workspace_member, methods=["PUT"])
    router.add_api_route("/{workspace_id}/members/{user_id}", get_workspace_member, methods=["GET"])
    return router
