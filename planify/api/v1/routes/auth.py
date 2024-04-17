from typing import Annotated

from fastapi import APIRouter, Depends, Request

from planify.api.dependencies import AuthProvider, get_auth_provider, current_user
from planify.api.models.auth import Tokens, UserLogin, RefreshTokenCreate, UserRefresh, JwtToken
from planify.api.utils.auth import RefreshTokenHeader
from planify.api.utils.request import get_ipaddr
from planify.core.models import dto
from planify.infrastructure.db.dao.holder import HolderDAO
from planify.infrastructure.di.db import dao_provider

refresh = RefreshTokenHeader()


async def login(
    request: Request,
    login_data: UserLogin,
    dao: Annotated[HolderDAO, Depends(dao_provider)],
    auth_provider: Annotated[AuthProvider, Depends(get_auth_provider)],
) -> Tokens:
    user = await auth_provider.properties.authenticate_user(
        username=login_data.username,
        password=login_data.password,
        dao=dao.user,
    )
    tokens = await auth_provider.properties.create_user_tokens(
        user=user,
        refresh_model=RefreshTokenCreate(
            fingerprint=login_data.fingerprint,
            ip=get_ipaddr(request),
            device=request.headers.get("User-Agent", ""),
        ),
        dao=dao,
    )
    await dao.commit()
    return tokens


async def logout(
    refresh_token: Annotated[JwtToken, Depends(refresh)],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
    auth_provider: Annotated[AuthProvider, Depends(get_auth_provider)],
) -> None:
    await dao.refresh_session.remove_by_id(
        auth_provider.properties.get_refresh_session_id_by_token(refresh_token.token)
    )
    await dao.commit()
    return None


async def logout_all(
    user: Annotated[dto.User, Depends(current_user)],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
) -> None:
    await dao.refresh_session.remove_by_user_id(user.id)
    await dao.commit()
    return None


async def refresh(
    request: Request,
    refresh_data: UserRefresh,
    refresh_token: Annotated[JwtToken, Depends(refresh)],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
    auth_provider: Annotated[AuthProvider, Depends(get_auth_provider)],
) -> Tokens:
    tokens = await auth_provider.properties.refresh_user_tokens(
        refresh_token=refresh_token,
        refresh_model=RefreshTokenCreate(
            fingerprint=refresh_data.fingerprint,
            ip=get_ipaddr(request),
            device=request.headers.get("User-Agent", ""),
        ),
        dao=dao,
    )
    await dao.commit()
    return tokens


def setup() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["auth"])
    router.add_api_route("/login", login, methods=["POST"])
    router.add_api_route("/logout", logout, methods=["POST"])
    router.add_api_route("/logoutAll", logout_all, methods=["POST"])
    router.add_api_route("/refresh", refresh, methods=["POST"])
    return router
