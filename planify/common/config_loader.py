from datetime import timedelta

from envparse import Env
from sqlalchemy.util import EMPTY_DICT

from planify.api.config import ApiConfig, AuthConfig
from planify.infrastructure.config.db import DbConfig, DbEngineConfig, DbConnectConfig


class ConfigLoader:
    def __init__(self, prefix: str = ""):
        self.env = Env()
        self._prefix = prefix

    @property
    def api_config(self) -> ApiConfig:
        return ApiConfig(
            auth=AuthConfig(
                secret_key=self.env.str(self._prefix + "SECRET_KEY"),
                algorithm=self.env.str(self._prefix + "ALGORITHM", default="HS256"),
                access_token_expiration=timedelta(
                    minutes=self.env.int(self._prefix + "ACCESS_TOKEN_EX_MINUTES", default=30)
                ),
                refresh_token_expiration=timedelta(
                    days=self.env.int(self._prefix + "REFRESH_TOKEN_EX_DAYS", default=30)
                ),
                max_refresh_sessions_count=self.env.int(self._prefix + "MAX_REFRESH_SESSIONS_COUNT", default=5),
            ),
            enable_logging=self.env.bool(self._prefix + "ENABLE_LOGGING", default=False),
        )

    @property
    def db_config(self) -> DbConfig:
        return DbConfig(
            connect=DbConnectConfig(
                type=self.env.str(self._prefix + "DB_TYPE", default="postgresql"),
                connector=self.env.str(self._prefix + "DB_CONNECTOR", default="asyncpg"),
                host=self.env.str(self._prefix + "DB_HOST", default="localhost"),
                port=self.env.int(self._prefix + "DB_PORT", default=5432),
                username=self.env.str(self._prefix + "DB_USERNAME"),
                password=self.env.str(self._prefix + "DB_PASSWORD"),
                database=self.env.str(self._prefix + "DB_DATABASE"),
                query=self.env.dict(self._prefix + "DB_QUERY", default=EMPTY_DICT),
            ),
            engine=DbEngineConfig(
                pool_size=self.env.int(self._prefix + "DB_POOL_SIZE", default=10),
                max_overflow=self.env.int(self._prefix + "DB_MAX_OVERFLOW", default=5),
                pool_recycle=self.env.int(self._prefix + "DB_POOL_RECYCLE", default=600),
                pool_pre_ping=self.env.bool(self._prefix + "DB_POOL_PRE_PING", default=True),
                pool_use_lifo=self.env.bool(self._prefix + "DB_POOL_USE_LIFO", default=True),
                pool_timeout=self.env.int(self._prefix + "DB_POOL_TIMEOUT", default=60),
            ),
        )
