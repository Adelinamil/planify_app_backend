from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from planify.core.models import dto
from planify.core.models.enums.task import TaskStatus, TaskPriority


class CreateTaskModel(BaseModel):
    name: str
    status: TaskStatus = TaskStatus.OPEN
    priority: TaskPriority = TaskPriority.MEDIUM

    def to_dto(self, author_id: UUID, workspace_id: int) -> dto.Task:
        return dto.Task(
            id=None,
            name=self.name,
            author_id=author_id,
            workspace_id=workspace_id,
            status=self.status,
            priority=self.priority,
        )


class EditTaskModel(BaseModel):
    name: str
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    deadline: datetime | None = None
    author_id: UUID | None = None
    performer_id: UUID | None = None
    project_id: int | None = None

    def to_dto(self, task_id: int, workspace_id: int) -> dto.Task:
        return dto.Task(
            id=task_id,
            name=self.name,
            description=self.description,
            status=self.status,
            priority=self.priority,
            deadline=self.deadline,
            performer_id=self.performer_id,
            author_id=self.author_id,
            project_id=self.project_id,
            workspace_id=workspace_id,
        )
