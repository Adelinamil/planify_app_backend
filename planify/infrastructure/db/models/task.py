import uuid
from datetime import datetime

from sqlalchemy import types, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from planify.core.models import dto
from planify.core.models.enums.task import TaskPriority, TaskStatus
from planify.infrastructure.db.models import Base
from planify.infrastructure.db.models.mixins import TimestampMixin
from planify.infrastructure.db.models.project import Project
from planify.infrastructure.db.models.user import User


class Task(TimestampMixin, Base):
    __tablename__ = "tasks"
    __mapper_args__ = {"eager_defaults": True}
    id: Mapped[int] = mapped_column(types.BigInteger, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(types.Text, nullable=False)
    description: Mapped[str] = mapped_column(types.Text, nullable=True)
    priority: Mapped[TaskPriority]
    status: Mapped[TaskStatus]
    deadline: Mapped[datetime] = mapped_column(types.DateTime(timezone=True), nullable=True)

    workspace_id: Mapped[int] = mapped_column(
        types.BigInteger,
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    project_id: Mapped[int] = mapped_column(
        types.BigInteger,
        ForeignKey("projects.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    author_id: Mapped[uuid.UUID] = mapped_column(
        types.UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
        nullable=False,
    )
    performer_id: Mapped[uuid.UUID] = mapped_column(
        types.UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )

    author: Mapped["User"] = relationship(foreign_keys=[author_id])
    performer: Mapped["User"] = relationship(foreign_keys=[performer_id])
    project: Mapped["Project"] = relationship(foreign_keys=[project_id])

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name})>"

    def to_dto(
        self,
        with_project: bool = False,
        with_author: bool = False,
        with_performer: bool = False,
    ) -> dto.Task:
        return dto.Task(
            id=self.id,
            name=self.name,
            priority=self.priority,
            status=self.status,
            description=self.description,
            deadline=self.deadline,
            workspace_id=self.workspace_id,
            project_id=self.project_id,
            author_id=self.author_id,
            performer_id=self.performer_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            author=self.author.to_dto() if with_author and self.author else None,
            performer=self.performer.to_dto() if with_performer and self.performer else None,
            project=self.project.to_dto() if with_project and self.project else None,
        )

    @classmethod
    def from_dto(cls, task: dto.Task) -> "Task":
        return cls(
            id=task.id,
            name=task.name,
            priority=task.priority,
            status=task.status,
            description=task.description,
            deadline=task.deadline,
            workspace_id=task.workspace_id,
            project_id=task.project_id,
            author_id=task.author_id,
            performer_id=task.performer_id,
        )
