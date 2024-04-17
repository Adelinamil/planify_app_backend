import logging
from datetime import timedelta
from typing import Annotated
from uuid import UUID, uuid4

import bcrypt
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from starlette import status

from planify.api.config import AuthConfig
from planify.api.models.auth import JwtToken, Tokens, RefreshTokenCreate
from planify.api.utils.auth import CustomAuthHeader
from planify.common import dt_utils
from planify.core.models import dto
from planify.core.services.refresh_session import add_refresh_session, verify_refresh_session
from planify.core.utils.exceptions import NoUsernameFound, InvalidRefreshSession
from planify.infrastructure.db.dao.holder import HolderDAO
from planify.infrastructure.db.dao.rdb import UserDAO
from planify.infrastructure.di.db import dao_provider

logger = logging.getLogger(__name__)

auth_header = CustomAuthHeader()


def get_auth_provider():
    raise NotImplementedError


def current_user(token: JwtToken = Depends(auth_header)):
    raise NotImplementedError


class AuthProperties:
    def __init__(self, config: AuthConfig) -> None:
        super().__init__()
        self._config = config
        self._secret_key = config.secret_key
        self._algorythm = "HS256"

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=plain_password.encode("utf-8"),
            hashed_password=hashed_password.encode("utf-8"),
        )

    def get_password_hash(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password=password.encode("utf-8"), salt=salt).decode("utf-8")

    async def authenticate_user(self, username: str, password: str, dao: UserDAO) -> dto.User:
        http_status_401 = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            user = await dao.get_by_username_with_password(username)
        except NoUsernameFound as e:
            raise http_status_401 from e
        if not self.verify_password(password, user.hashed_password or ""):
            raise http_status_401
        return user.without_password()

    def _get_jwt_token_sub(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorythm],
            )
            if payload.get("sub") is None:
                logger.warning("valid jwt contains no user id")
                raise credentials_exception

            return payload["sub"]
        except JWTError as e:
            logger.info("invalid jwt", exc_info=e)
            raise credentials_exception from e
        except Exception as e:
            logger.warning("some jwt error", exc_info=e)
            raise

    def _create_jwt_token(self, data: dict, expires_delta: timedelta) -> JwtToken:
        to_encode = data.copy()
        expires_in = dt_utils.now() + expires_delta
        to_encode.update({"exp": expires_in})
        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorythm)
        return JwtToken(token=encoded_jwt, token_type="Bearer", expires_in=expires_in)

    def get_refresh_session_id_by_token(self, refresh_token: str) -> UUID:
        try:
            return UUID(self._get_jwt_token_sub(refresh_token))
        except (ValueError, TypeError, AttributeError) as e:
            logger.warning("Cannot get refresh session id from token", exc_info=e)
            raise InvalidRefreshSession

    async def _create_tokens(
        self,
        user_id: UUID,
        refresh_model: RefreshTokenCreate,
        dao: HolderDAO,
    ) -> Tokens:
        new_refresh_session = await add_refresh_session(
            refresh_session=dto.RefreshSession(
                id=uuid4(),
                user_id=user_id,
                device=refresh_model.device,
                fingerprint=refresh_model.fingerprint,
                ip=refresh_model.ip,
                expires_in=dt_utils.now() + self._config.refresh_token_expiration,
            ),
            dao=dao.refresh_session,
            max_refresh_sessions_count=self._config.max_refresh_sessions_count,
        )
        return Tokens(
            access=self._create_jwt_token(
                data={"sub": str(new_refresh_session.user_id)},
                expires_delta=self._config.access_token_expiration,
            ),
            refresh=self._create_jwt_token(
                data={"sub": str(new_refresh_session.id)},
                expires_delta=self._config.refresh_token_expiration,
            ),
        )

    async def refresh_user_tokens(
        self,
        refresh_token: JwtToken,
        refresh_model: RefreshTokenCreate,
        dao: HolderDAO,
    ) -> Tokens:
        old_refresh_session = await verify_refresh_session(
            refresh_session_id=self.get_refresh_session_id_by_token(refresh_token.token),
            new_fingerprint=refresh_model.fingerprint,
            dao=dao.refresh_session,
        )
        tokens = await self._create_tokens(user_id=old_refresh_session.user_id, refresh_model=refresh_model, dao=dao)
        return tokens

    async def create_user_tokens(self, user: dto.User, refresh_model: RefreshTokenCreate, dao: HolderDAO) -> Tokens:
        tokens = await self._create_tokens(user_id=user.id, refresh_model=refresh_model, dao=dao)
        return tokens

    async def get_current_user(
        self,
        access_token: JwtToken,
        dao: UserDAO,
    ) -> dto.User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            user_id = UUID(self._get_jwt_token_sub(access_token.token))
        except (ValueError, TypeError, AttributeError) as e:
            logger.warning("Cannot get user id from token", exc_info=e)
            raise credentials_exception

        try:
            user = await dao.get_by_id(user_id)
        except Exception as e:
            logger.info(f"user by id {user_id} not found")
            raise credentials_exception from e
        return user


class AuthProvider:
    def __init__(self, config: AuthConfig):
        self._config = config
        self._properties = AuthProperties(config)

    @property
    def properties(self) -> AuthProperties:
        return self._properties

    async def get_current_user(
        self,
        token: Annotated[JwtToken, Depends(auth_header)],
        dao: Annotated[HolderDAO, Depends(dao_provider)],
    ) -> dto.User:
        return await self._properties.get_current_user(token, dao.user)
