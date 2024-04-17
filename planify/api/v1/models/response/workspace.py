from dataclasses import dataclass

from planify.core.models import dto
from planify.core.models.enums.workspace import WorkspaceMemberRole
from .user import UserResponseModel


@dataclass
class WorkspaceMemberResponseModel:
    user: UserResponseModel
    workspace_id: int
    role: WorkspaceMemberRole
    active: bool

    @classmethod
    def from_dto(cls, workspace_member_dto: dto.WorkspaceMember) -> "WorkspaceMemberResponseModel":
        return cls(
            user=UserResponseModel.from_dto(workspace_member_dto.user),
            workspace_id=workspace_member_dto.workspace_id,
            role=workspace_member_dto.role,
            active=workspace_member_dto.active,
        )
