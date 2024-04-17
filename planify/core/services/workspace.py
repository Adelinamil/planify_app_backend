from uuid import UUID

from planify.core.interfaces.dal.user import UserByIdResolver
from planify.core.interfaces.dal.workspace import WorkspaceCreator, WorkspaceEditor, WorkspaceRemover
from planify.core.interfaces.dal.workspace_member import WorkspaceMemberCreator, WorkspaceMemberEditor
from planify.core.models import dto
from planify.core.models.enums.workspace import WorkspaceMemberRole


async def create_workspace(
    user_id: UUID,
    workspace: dto.Workspace,
    workspace_dao: WorkspaceCreator,
    workspace_member_dao: WorkspaceMemberCreator,
) -> dto.Workspace:
    workspace_dto = await workspace_dao.create(workspace)
    await workspace_member_dao.create(
        dto.WorkspaceMember(
            user_id=user_id,
            workspace_id=workspace_dto.id,
            role=WorkspaceMemberRole.OWNER,
            active=True,
        )
    )
    await workspace_dao.commit()
    return workspace_dto


async def edit_workspace(workspace: dto.Workspace, workspace_dao: WorkspaceEditor) -> dto.Workspace:
    workspace_dto = await workspace_dao.update(workspace_dto=workspace)
    await workspace_dao.commit()
    return workspace_dto


async def remove_workspace(workspace_id: int, workspace_dao: WorkspaceRemover) -> None:
    await workspace_dao.remove(workspace_id)
    await workspace_dao.commit()
    return None


async def add_workspace_member(
    workspace_member: dto.WorkspaceMember,
    user_dao: UserByIdResolver,
    workspace_member_dao: WorkspaceMemberCreator,
) -> dto.WorkspaceMember:
    await user_dao.get_by_id(workspace_member.user_id)
    new_member_dto = await workspace_member_dao.create(workspace_member)
    await workspace_member_dao.commit()
    return new_member_dto


async def edit_workspace_member(
    workspace_member: dto.WorkspaceMember,
    workspace_member_dao: WorkspaceMemberEditor,
) -> dto.WorkspaceMember:
    await workspace_member_dao.update(workspace_member)
    await workspace_member_dao.commit()
    return workspace_member
