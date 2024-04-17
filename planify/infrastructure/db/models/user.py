import uuid

from sqlalchemy import types
from sqlalchemy.orm import mapped_column, Mapped

from planify.core.models import dto
from planify.infrastructure.db.models.base import Base
from planify.infrastructure.db.models.mixins import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}
    id: Mapped[uuid.UUID] = mapped_column(types.UUID(as_uuid=True), primary_key=True)
    username: Mapped[str] = mapped_column(types.Text, unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(types.Text, nullable=True)
    last_name: Mapped[str] = mapped_column(types.Text, nullable=True)
    email: Mapped[str] = mapped_column(types.Text, unique=True, nullable=True)
    phone: Mapped[str] = mapped_column(types.Text, unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(types.Text, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

    def to_dto(self) -> dto.User:
        return dto.User(
            id=self.id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_dto(cls, user: dto.User) -> "User":
        return cls(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
