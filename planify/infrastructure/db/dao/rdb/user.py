from uuid import UUID

from sqlalchemy import select, ScalarResult, Result
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from planify.core.models import dto
from planify.core.utils.exceptions import NoUsernameFound, UserExists, NoUserFound
from planify.infrastructure.db.models import User
from .base import BaseDAO


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_id(self, id_: UUID) -> dto.User:
        try:
            return (await self._get_by_id(id_)).to_dto()
        except NoResultFound as e:
            raise NoUserFound from e

    async def get_by_username(self, username: str) -> dto.User:
        return (await self._get_by_username(username)).to_dto()

    async def get_by_username_with_password(self, username: str) -> dto.UserWithCredentials:
        user = await self._get_by_username(username)
        return user.to_dto().add_password(user.hashed_password)

    async def _get_by_username(self, username: str) -> User:
        result: Result[tuple[User]] = await self._session.execute(select(User).where(User.username == username))
        try:
            user = result.scalar_one()
        except NoResultFound as e:
            raise NoUsernameFound from e
        return user

    async def search_by_username(self, username: str, offset: int, limit: int) -> list[dto.User]:
        result: ScalarResult[User] = await self._session.scalars(
            select(User).where(User.username.ilike(f"%{username}%")).limit(limit).offset(offset)
        )
        return [user.to_dto() for user in result.all()]

    async def create(self, user_dto: dto.UserWithCredentials) -> dto.User:
        user = User.from_dto(user_dto)
        user.hashed_password = user_dto.hashed_password
        self._save(user)
        try:
            await self._flush(user)
        except IntegrityError as e:
            raise UserExists from e
        else:
            return user.to_dto()

    async def get_users(self, offset: int, limit: int) -> list[dto.User]:
        result: ScalarResult[User] = await self._session.scalars(select(User).offset(offset).limit(limit))
        return [user.to_dto() for user in result.all()]
