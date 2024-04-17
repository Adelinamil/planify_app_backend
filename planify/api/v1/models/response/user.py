from dataclasses import dataclass
from uuid import UUID

from planify.core.models import dto


@dataclass
class UserResponseModel:
    id: UUID
    username: str
    first_name: str | None = None
    last_name: str | None = None

    @classmethod
    def from_dto(cls, user_dto: dto.User) -> "UserResponseModel":
        return cls(
            id=user_dto.id,
            username=user_dto.username,
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
        )
