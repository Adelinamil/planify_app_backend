from uuid import UUID

from planify.core.interfaces.dal.workspace_member import IsWorkspaceMemberResolver
from planify.core.utils.exceptions import NoWorkspaceMemberFound


async def is_members(members: list[UUID], workspace_id: int, dao: IsWorkspaceMemberResolver):
    for user_id in members:
        if user_id is not None and not await dao.is_member(
            user_id=user_id,
            workspace_id=workspace_id,
        ):
            raise NoWorkspaceMemberFound
