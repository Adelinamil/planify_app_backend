from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import Field

from planify.api.dependencies.auth import get_auth_provider, AuthProvider, current_user
from planify.api.v1.models.response.user import UserResponseModel
from planify.api.v1.models.validation.user import CreateUserModel
from planify.core.models import dto
from planify.core.services import user as services
from planify.infrastructure.db.dao.holder import HolderDAO
from planify.infrastructure.di.db import dao_provider


async def get_current_user(user: Annotated[dto.User, Depends(current_user)]) -> dto.User:
    return user


async def search_users(
    username: Annotated[str, Field(min_length=3, max_length=16, pattern="^[a-zA-Z0-9_]+$")],
    user: Annotated[dto.User, Depends(current_user)],
    dao: Annotated[HolderDAO, Depends(dao_provider)],
    offset: int = Query(default=0),
    limit: int = Query(default=10),
) -> list[UserResponseModel]:
    return [
        UserResponseModel.from_dto(user_dto)
        for user_dto in await dao.user.search_by_username(username=username, offset=offset, limit=limit)
    ]


async def create_user(
    user: CreateUserModel,
    dao: Annotated[HolderDAO, Depends(dao_provider)],
    auth_provider: Annotated[AuthProvider, Depends(get_auth_provider)],
) -> dto.User:
    return await services.create_user(
        user=user.to_dto(),
        hashed_password=auth_provider.properties.get_password_hash(user.password),
        dao=dao.user,
    )


def setup() -> APIRouter:
    router = APIRouter(prefix="/users", tags=["users"])
    router.add_api_route("/current", get_current_user, methods=["GET"])
    router.add_api_route("/create", create_user, methods=["POST"])
    router.add_api_route("/search", search_users, methods=["GET"])
    return router
