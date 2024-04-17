import uuid

from sqlalchemy import types, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from planify.core.models import dto
from planify.infrastructure.db.models import Base
from planify.infrastructure.db.models.mixins import TimestampMixin
from planify.infrastructure.db.models.user import User


class Project(TimestampMixin, Base):
    __tablename__ = "projects"
    __mapper_args__ = {"eager_defaults": True}
    id: Mapped[int] = mapped_column(types.BigInteger, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(types.Text, nullable=False)
    description: Mapped[str] = mapped_column(types.Text, nullable=True)
    workspace_id: Mapped[int] = mapped_column(
        types.BigInteger,
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    author_id: Mapped[uuid.UUID] = mapped_column(
        types.UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    manager_id: Mapped[uuid.UUID] = mapped_column(
        types.UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    author: Mapped["User"] = relationship(foreign_keys=[author_id])
    manager: Mapped["User"] = relationship(foreign_keys=[manager_id])

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name})>"

    def to_dto(self, with_author: bool = False, with_manager: bool = False) -> dto.Project:
        return dto.Project(
            id=self.id,
            name=self.name,
            description=self.description,
            workspace_id=self.workspace_id,
            author_id=self.author_id,
            manager_id=self.manager_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            author=self.author.to_dto() if with_author and self.author else None,
            manager=self.manager.to_dto() if with_manager and self.manager else None,
        )

    @classmethod
    def from_dto(cls, workspace: dto.Project) -> "Project":
        return cls(
            id=workspace.id,
            name=workspace.name,
            description=workspace.description,
            workspace_id=workspace.workspace_id,
            author_id=workspace.author_id,
            manager_id=workspace.manager_id,
        )


class ProjectMember(Base):
    __tablename__ = "project_members"
    __mapper_args__ = {"eager_defaults": True}
    user_id: Mapped[uuid.UUID] = mapped_column(
        types.UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        primary_key=True,
    )
    project_id: Mapped[int] = mapped_column(
        types.BigInteger,
        ForeignKey("projects.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        primary_key=True,
    )

    user: Mapped["User"] = relationship()

    def __repr__(self):
        return f"<ProjectMember(user_id={self.user_id}, project_id={self.project_id})>"

    def to_dto(self, with_user: bool = False) -> dto.ProjectMember:
        return dto.ProjectMember(
            user_id=self.user_id, project_id=self.project_id, user=self.user.to_dto() if with_user else None
        )

    @classmethod
    def from_dto(cls, project_member: dto.ProjectMember) -> "ProjectMember":
        return cls(user_id=project_member.user_id, project_id=project_member.project_id)
