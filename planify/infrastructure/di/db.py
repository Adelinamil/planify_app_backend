from typing import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from planify.infrastructure.config.db import DbConfig
from planify.infrastructure.db.dao.holder import HolderDAO


def dao_provider() -> HolderDAO:
    raise NotImplementedError


class DbProvider:
    def __init__(self, config: DbConfig):
        self._config = config
        self._engine: AsyncEngine = create_async_engine(config.connect.url)
        self._pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
        )

    async def get_dao(self) -> AsyncIterable[HolderDAO]:
        async with self._pool() as session:
            yield HolderDAO(session=session)

    async def shutdown(self):
        await self._engine.dispose()
