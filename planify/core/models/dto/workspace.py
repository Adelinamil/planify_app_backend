from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .user import User
from ..enums.workspace import WorkspaceMemberRole


@dataclass
class Workspace:
    id: int | None
    name: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class WorkspaceMember:
    user_id: UUID
    workspace_id: int
    role: WorkspaceMemberRole
    active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    user: User | None = None
