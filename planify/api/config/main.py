from dataclasses import dataclass

from .auth import AuthConfig


@dataclass(frozen=True)
class ApiConfig:
    auth: AuthConfig
    enable_logging: bool = False
