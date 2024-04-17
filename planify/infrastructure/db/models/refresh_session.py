import uuid
from datetime import datetime

from sqlalchemy import types, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from planify.core.models import dto
from planify.infrastructure.db.models.base import Base
from planify.infrastructure.db.models.mixins import TimestampMixin


class RefreshSession(TimestampMixin, Base):
    __tablename__ = "refresh_sessions"
    __mapper_args__ = {"eager_defaults": True}
    id: Mapped[uuid.UUID] = mapped_column(types.UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        types.UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    device: Mapped[str] = mapped_column(types.Text, nullable=False)
    fingerprint: Mapped[uuid.UUID] = mapped_column(types.UUID(as_uuid=True), nullable=False)
    ip: Mapped[str] = mapped_column(types.String(length=15), nullable=False)
    expires_in: Mapped[datetime] = mapped_column(types.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return f"<RefreshSession(id={self.id}, user_id={self.user_id})>"

    def to_dto(self) -> dto.RefreshSession:
        return dto.RefreshSession(
            id=self.id,
            user_id=self.user_id,
            device=self.device,
            fingerprint=self.fingerprint,
            ip=self.ip,
            expires_in=self.expires_in,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_dto(cls, refresh_session: dto.RefreshSession) -> "RefreshSession":
        return cls(
            id=refresh_session.id,
            user_id=refresh_session.user_id,
            device=refresh_session.device,
            fingerprint=refresh_session.fingerprint,
            ip=refresh_session.ip,
            expires_in=refresh_session.expires_in,
        )
