import re
from uuid import uuid4

from pydantic import BaseModel, model_validator, EmailStr, constr, field_validator, Field

from planify.core.models import dto

PASSWORD_PATTERN = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).+$"
PASSWORD_VALIDATION_MESSAGE = """
Password must contain at least one digit, one uppercase letter, one lowercase letter, one special character,
 and be at least 8 characters long
"""


class CreateUserModel(BaseModel):
    username: constr(strip_whitespace=True, min_length=3, max_length=16) = Field(pattern="^[a-zA-Z0-9_]+$")
    password: constr(strip_whitespace=True, min_length=8, max_length=32) = Field(
        description=f"matches {PASSWORD_PATTERN}"
    )
    first_name: constr(strip_whitespace=True, min_length=1, max_length=100) | None = None
    last_name: constr(strip_whitespace=True, min_length=1, max_length=100) | None = None
    email: EmailStr | None = None
    phone: constr(strip_whitespace=True, min_length=1, max_length=20) | None = Field(default=None, pattern=r"^\d+$")

    @field_validator("password")
    @classmethod
    def password_regex(cls, v: str) -> str:
        if not re.match(PASSWORD_PATTERN, v):
            raise ValueError(PASSWORD_VALIDATION_MESSAGE)
        return v

    @model_validator(mode="after")
    def check_email_or_phone(self) -> "CreateUserModel":
        if self.email is None and self.phone is None:
            raise ValueError("Please provide either email or phone")
        return self

    def to_dto(self) -> dto.User:
        return dto.User(
            id=uuid4(),
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone,
        )
