from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class AuthConfig:
    secret_key: str
    algorithm: str
    access_token_expiration: timedelta
    refresh_token_expiration: timedelta
    max_refresh_sessions_count: int
