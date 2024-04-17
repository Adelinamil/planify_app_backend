from collections.abc import Sequence
from typing import TypeVar, Generic
from uuid import UUID

from sqlalchemy import delete, func, ScalarResult
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from planify.infrastructure.db.models import Base

Model = TypeVar("Model", bound=Base, covariant=True, contravariant=False)


class BaseDAO(Generic[Model]):
    def __init__(self, model: type[Model], session: AsyncSession):
        self._model = model
        self._session = session

    async def _get_all(self, options: Sequence[ORMOption] = ()) -> Sequence[Model]:
        result: ScalarResult[Model] = await self._session.scalars(select(self._model).options(*options))
        return result.all()

    async def _get_by_id(
        self,
        id_: UUID | int | tuple,
        options: Sequence[ORMOption] | None = None,
        populate_existing: bool = False,
    ) -> Model:
        result = await self._session.get(self._model, id_, options=options, populate_existing=populate_existing)
        if result is None:
            raise NoResultFound
        return result

    async def _remove_by_id(self, id_: UUID | int):
        await self._session.execute(delete(self._model).where(self._model.id == id_))

    def _save(self, obj: Base):
        self._session.add(obj)

    async def delete_all(self):
        await self._session.execute(delete(self._model))

    async def _delete(self, obj: Base):
        await self._session.delete(obj)

    async def count(self):
        result = await self._session.execute(select(func.count(self._model.id)))
        return result.scalar_one()

    async def commit(self):
        await self._session.commit()

    async def _flush(self, *objects: Base):
        await self._session.flush(objects)
