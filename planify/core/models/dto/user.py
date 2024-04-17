from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    username: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def fullname(self) -> str:
        if self.first_name is None:
            return ""
        if self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    def add_password(self, hashed_password: str) -> UserWithCredentials:
        return UserWithCredentials(
            id=self.id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone,
            hashed_password=hashed_password,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


@dataclass
class UserWithCredentials(User):
    hashed_password: str | None = None

    def without_password(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
