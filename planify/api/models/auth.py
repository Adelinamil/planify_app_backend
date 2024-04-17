from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class JwtToken(BaseModel):
    token: str
    token_type: str
    expires_in: datetime | None = None


class Tokens(BaseModel):
    access: JwtToken
    refresh: JwtToken


class RefreshTokenCreate(BaseModel):
    fingerprint: UUID
    ip: str
    device: str


class UserLogin(BaseModel):
    username: str
    password: str
    fingerprint: UUID


class UserRefresh(BaseModel):
    fingerprint: UUID
