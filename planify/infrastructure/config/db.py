from dataclasses import dataclass
from typing import Mapping, Sequence

from sqlalchemy import URL


@dataclass(frozen=True)
class DbConnectConfig:
    type: str
    connector: str
    host: str
    port: int
    username: str
    password: str
    database: str
    query: Mapping[str, Sequence[str] | str]

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=f"{self.type}+{self.connector}",
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            query=self.query,
        )


@dataclass(frozen=True)
class DbEngineConfig:
    pool_size: int
    max_overflow: int
    pool_recycle: int
    pool_pre_ping: bool
    pool_use_lifo: bool
    pool_timeout: int


@dataclass(frozen=True)
class DbConfig:
    connect: DbConnectConfig
    engine: DbEngineConfig
