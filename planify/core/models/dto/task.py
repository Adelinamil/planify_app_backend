from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from planify.core.models.dto.project import Project
from planify.core.models.dto.user import User
from planify.core.models.enums.task import TaskPriority, TaskStatus


@dataclass
class Task:
    id: int | None
    name: str
    priority: TaskPriority
    status: TaskStatus
    workspace_id: int
    description: str | None = None
    deadline: datetime | None = None
    project_id: int | None = None
    author_id: UUID | None = None
    performer_id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    author: User | None = None
    performer: User | None = None
    project: Project | None = None
