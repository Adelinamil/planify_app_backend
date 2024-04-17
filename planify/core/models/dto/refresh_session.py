from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class RefreshSession:
    id: UUID
    user_id: UUID
    device: str
    fingerprint: UUID
    ip: str
    expires_in: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
