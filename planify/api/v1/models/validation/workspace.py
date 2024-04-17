from enum import Enum
from uuid import UUID

from pydantic import BaseModel, constr

from planify.core.models import dto
from planify.core.models.enums.workspace import WorkspaceMemberRole


class WorkspaceModel(BaseModel):
    name: constr(min_length=1, max_length=50)

    def to_dto(self, workspace_id: int | None = None) -> dto.Workspace:
        return dto.Workspace(id=workspace_id, name=self.name)


class CreateWorkspaceModel(WorkspaceModel):
    pass


class EditWorkspaceModel(WorkspaceModel):
    pass


class AddWorkspaceMemberRole(Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class AddMemberModel(BaseModel):
    user_id: UUID
    role: AddWorkspaceMemberRole

    def to_dto(self, workspace_id: int) -> dto.WorkspaceMember:
        return dto.WorkspaceMember(
            user_id=self.user_id,
            workspace_id=workspace_id,
            role=WorkspaceMemberRole(self.role.value),
            active=True,
        )


class EditMemberModel(AddMemberModel):
    role: AddWorkspaceMemberRole
    active: bool

    def to_dto(self, workspace_id: int) -> dto.WorkspaceMember:
        return dto.WorkspaceMember(
            user_id=self.user_id,
            workspace_id=workspace_id,
            role=WorkspaceMemberRole(self.role.value),
            active=self.active,
        )
