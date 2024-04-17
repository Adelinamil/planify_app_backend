from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .user import User


@dataclass
class Project:
    id: int | None
    name: str
    workspace_id: int
    description: str | None = None
    author_id: UUID | None = None
    manager_id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    author: User | None = None
    manager: User | None = None


@dataclass
class ProjectMember:
    user_id: UUID
    project_id: int

    user: User | None = None
