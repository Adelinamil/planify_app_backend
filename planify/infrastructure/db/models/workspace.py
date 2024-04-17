import uuid

from sqlalchemy import types, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from planify.core.models import dto
from planify.core.models.enums.workspace import WorkspaceMemberRole
from planify.infrastructure.db.models import Base
from planify.infrastructure.db.models.mixins import TimestampMixin
from planify.infrastructure.db.models.user import User


class Workspace(TimestampMixin, Base):
    __tablename__ = "workspaces"
    __mapper_args__ = {"eager_defaults": True}
    id: Mapped[int] = mapped_column(types.BigInteger, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(types.Text, nullable=False)

    def __repr__(self):
        return f"<Workspace(id={self.id}, name={self.name})>"

    def to_dto(self) -> dto.Workspace:
        return dto.Workspace(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_dto(cls, workspace: dto.Workspace) -> "Workspace":
        return cls(
            id=workspace.id,
            name=workspace.name,
            created_at=workspace.created_at,
            updated_at=workspace.updated_at,
        )


class WorkspaceMember(TimestampMixin, Base):
    __tablename__ = "workspace_members"
    __mapper_args__ = {"eager_defaults": True}
    user_id: Mapped[uuid.UUID] = mapped_column(
        types.UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        primary_key=True,
    )
    workspace_id: Mapped[int] = mapped_column(
        types.BigInteger,
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        primary_key=True,
    )
    role: Mapped[WorkspaceMemberRole]
    active: Mapped[bool] = mapped_column(types.Boolean, nullable=False, default=True)

    user: Mapped["User"] = relationship()

    def __repr__(self):
        return (
            f"<WorkspaceMember(user_id={self.user_id}, workspace_id={self.workspace_id}, "
            f"role={self.role}, active={self.active})>"
        )

    def to_dto(self, with_user: bool = False) -> dto.WorkspaceMember:
        return dto.WorkspaceMember(
            user_id=self.user_id,
            workspace_id=self.workspace_id,
            role=self.role,
            active=self.active,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user=self.user.to_dto() if with_user else None,
        )

    @classmethod
    def from_dto(cls, workspace_member: dto.WorkspaceMember) -> "WorkspaceMember":
        return cls(
            user_id=workspace_member.user_id,
            workspace_id=workspace_member.workspace_id,
            role=workspace_member.role,
            active=workspace_member.active,
            created_at=workspace_member.created_at,
            updated_at=workspace_member.updated_at,
        )
