from typing import Annotated

from fastapi import Depends

from planify.api.dependencies.auth import current_user
from planify.core.models import dto
from planify.core.models.enums.workspace import WorkspaceMemberRole
from planify.core.utils.exceptions import NoWorkspaceFound
from planify.infrastructure.db.dao.holder import HolderDAO
from planify.infrastructure.di.db import dao_provider


def check_workspace(roles: list[WorkspaceMemberRole] | None = None):
    async def wrapper(
        workspace_id: int,
        user: Annotated[dto.User, Depends(current_user)],
        dao: Annotated[HolderDAO, Depends(dao_provider)],
    ) -> int:
        if not await dao.workspace_member.is_member(user_id=user.id, workspace_id=workspace_id, roles=roles):
            raise NoWorkspaceFound
        return workspace_id

    return wrapper
