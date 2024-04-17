from uuid import UUID

from sqlalchemy import Result, select, delete, func, and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from planify.common import dt_utils
from planify.core.models import dto
from planify.core.utils.exceptions import NoRefreshSessionFound
from planify.infrastructure.db.dao.rdb.base import BaseDAO
from planify.infrastructure.db.models import RefreshSession


class RefreshSessionDAO(BaseDAO[RefreshSession]):
    def __init__(self, session: AsyncSession):
        super().__init__(RefreshSession, session)

    async def get_by_id(self, id_: UUID) -> dto.RefreshSession:
        try:
            return (await self._get_by_id(id_)).to_dto()
        except NoResultFound as e:
            raise NoRefreshSessionFound from e

    async def create(self, refresh_session_dto: dto.RefreshSession) -> dto.RefreshSession:
        refresh_session = RefreshSession.from_dto(refresh_session_dto)
        self._save(refresh_session)
        await self._flush(refresh_session)
        return refresh_session.to_dto()

    async def remove_by_id(self, id_: UUID) -> int:
        result: Result[tuple[int]] = await self._session.execute(
            delete(RefreshSession).where(RefreshSession.id == id_).returning(RefreshSession.id)
        )
        try:
            return result.scalar_one()
        except NoResultFound as e:
            raise NoRefreshSessionFound from e

    async def remove_oldest_by_user_id(self, user_id: UUID):
        await self._session.execute(
            delete(RefreshSession).where(
                RefreshSession.id.in_(
                    select(RefreshSession.id)
                    .where(and_(RefreshSession.user_id == user_id, RefreshSession.expires_in > dt_utils.now()))
                    .order_by(RefreshSession.created_at)
                    .limit(1)
                )
            )
        )

    async def remove_by_user_id(self, user_id: UUID):
        await self._session.execute(delete(RefreshSession).where(RefreshSession.user_id == user_id))

    async def count_by_user_id(self, user_id: UUID) -> int:
        return await self._session.scalar(
            select(func.count(RefreshSession.id)).where(RefreshSession.user_id == user_id)
        )
